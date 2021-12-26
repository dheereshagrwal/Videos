from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.sites.shortcuts import get_current_site
from store.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {'products': products, }
    return render(request, 'home.html', context)

def login(request):
    return render(request, 'accounts/login.html')

def register():
    return redirect('login')

@login_required(login_url='login')
def logout(request):
    logout(request)


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
