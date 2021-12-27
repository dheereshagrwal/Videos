from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from store.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.views import _get_cart_id
from cart.models import Cart, CartItem


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {'products': products, }
    return render(request, 'home.html', context)


def login(request):
    user = auth.authenticate(request.user)
    print("user is: ", user)
    if user is not None:
        try:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(cart=cart)
                product_variations = []
                # Getting product variantions from cart id
                for item in cart_item:
                    variation = item.variations.all()
                    product_variations.append(list(variation))

                # Get the cart items from the users to access their product variations
                cart_item = CartItem.objects.filter(user=user)
                existing_variations_list = []
                id = []
                for item in cart_item:
                    existing_variations = item.variations.all()
                    existing_variations_list.append(list(existing_variations))
                    id.append(item.id)

                for product_variation in product_variations:
                    if product_variation in existing_variations_list:
                        index = existing_variations_list.index(
                            product_variation)
                        item_id = id[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()
        except:
            pass
        auth.login(user)
        return redirect('dashboard')
    else:
        return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')
