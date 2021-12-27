from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from store.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.views import _get_cart_id
from cart.models import Cart, CartItem


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {'products': products, }
    return render(request, 'home.html', context)


def login(request):
    user = auth.authenticate(request.user)
    print("user is: ",user)
    if user is not None:
        try:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            if is_cart_item_exists:
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
    # return render(request, 'accounts/login.html')


def register():
    return redirect('login')


@login_required(login_url='login')
def logout(request):
    logout(request)


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
