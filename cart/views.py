from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
# Create your views here.


def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, quantity=1, cart=cart)
        cart_item.save()
    if cart_item.quantity > 1:
        return redirect('cart')
    else:
        return redirect(str(product.get_url()))


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        delivery_charge = 0
        gift_wrap_charge = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total = total+gift_wrap_charge
        if grand_total >= 500:
            delivery_charge = 0
        else:
            delivery_charge = 50
        grand_total = total+delivery_charge+gift_wrap_charge

    except ObjectDoesNotExist:
        pass
    context = {"total": total, 'quantity': quantity, 'cart_items': cart_items,
               'delivery_charge': delivery_charge, 'gift_wrap_charge': gift_wrap_charge, 'grand_total': grand_total, }
    return render(request, 'store/cart.html', context)
