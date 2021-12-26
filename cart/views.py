from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.


def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(
        product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        # existing variations
        # current variations
        # item_id from database
        existing_variations_list = []
        id = []
        for item in cart_item:
            existing_variations = item.variations.all()
            existing_variations_list.append(list(existing_variations))
            id.append(item.id)

        if product_variation in existing_variations_list:
            # increase cart item quantity
            index = existing_variations_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item=CartItem.objects.create(product=product, quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    try:
        if item.quantity > 1:
            return redirect('cart')
        else:
            return redirect(str(product.get_url()))
    except:
        return redirect(str(product.get_url()))



def remove_cart(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
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
