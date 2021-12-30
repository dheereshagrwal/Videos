from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from store.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.views import _get_cart_id
from cart.models import Cart, CartItem
import requests
from order.models import Order, OrderProduct
# from .forms import UserForm, UserProfileForm
# from .models import UserProfile
from django import forms


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

                # Create user profile
                # form = UserForm(request.POST)
                # if form.is_valid():
                #     profile=UserProfile()
                #     profile.user_id = user.id
                #     profile.profile_picture='images/default/default-user.jpg'
                #     profile.save()

        except:
            pass
        auth.login(user)
        url = requests.META.get('HTTP_REFERER')
        try:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'next' in params:
                nextPage = params['next']
                return redirect(nextPage)
        except:
            return redirect('dashboard')
    else:
        return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by(
        '-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    # userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {'orders_count': orders_count}
    # context = {'orders_count': orders_count,'userprofile':userprofile}

    return render(request, 'dashboard.html', context)


def my_orders(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'my-orders.html', context)


# def edit_profile(request):
#     userprofile = get_object_or_404(UserProfile, user=request.user)
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         user_profile_form = UserProfileForm(
#             request.POST, request.FILES, instance=userprofile)
#         if user_form.is_valid() and user_profile_form.is_valid():
#             user_form.save()
#             user_profile_form.save()
#             messages.success(request, 'Your profile has been updated.')
#             return redirect('edit_profile')
#         else:
#             user_form = UserForm(instance=request.user)
#             user_profile_form = UserProfileForm(instance=userprofile)
#     context = {'user_form': user_form,'user_profile_form': user_profile_form,'userprofile':userprofile}
#     return render(request, 'edit-profile.html',context)

@login_required(login_url='login')
def order_details(request, order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price*i.quantity

    context = {'order_details': order_details,
               'order': order, 'subtotal': subtotal}
    return render(request, 'order/order-details.html', context)
