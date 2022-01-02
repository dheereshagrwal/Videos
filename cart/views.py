from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_get_cart_id(request))
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
                    # print(str(product_variation[3]))
                    if str(variation) == "Yes":
                        cart.cart_gift_charge = cart.cart_gift_charge + 10
                        cart.save()
                except:
                    pass
        # Do cart items exist for this product?
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=request.user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=request.user)
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
                item = CartItem.objects.create(
                    product=product, quantity=1, user=request.user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, user=request.user)
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
    # *User is not authenticated
    else:
        product = Product.objects.get(id=product_id)
        product_variation = []
        try:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_get_cart_id(request))
        cart.save()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    if str(variation) == "Yes":
                        cart.cart_gift_charge = cart.cart_gift_charge + 10
                        cart.save()
                        print('Inside add cart ', cart.cart_gift_charge)
                except:
                    pass
        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            existing_variations_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variations_list.append(list(existing_variations))
                id.append(item.id)
            # Grouping the product variations
            if product_variation in existing_variations_list:
                # increase cart item quantity
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
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


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            if cart.cart_gift_charge >= 10:
                cart.cart_gift_charge = cart.cart_gift_charge - 10
                print('Inside decrement cart ', cart.cart_gift_charge)
                cart.save()
            cart_item.quantity -= 1
            cart_item.save()
        else:
            if cart.cart_gift_charge >= 10:
                cart.cart_gift_charge = cart.cart_gift_charge - 10
                print('Inside decrement cart else ', cart.cart_gift_charge)
                cart.save()
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
        print(cart_item.quantity)
        for i in range(cart_item.quantity):
            if cart.cart_gift_charge >= 10:
                cart.cart_gift_charge = cart.cart_gift_charge - 10
            print('Inside whole remove ', cart.cart_gift_charge)
            cart.save()
    else:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        print(cart_item.quantity)
        for i in range(cart_item.quantity):
            if cart.cart_gift_charge >= 10:
                cart.cart_gift_charge = cart.cart_gift_charge - 10
                print('Inside whole remove ', cart.cart_gift_charge)
                cart.save()
    cart_item.delete()
    return redirect('cart')


coupon_codes = {'anime10': 0.1, 'anime20': 0.2, 'anime30': 0.3}


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        grand_total = 0
        discount_value = 0
        if request.user.is_authenticated:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total = total + (cart_item.product.price *
                             cart_item.quantity)
            cart.cart_subtotal = total
            cart.save()
            quantity += cart_item.quantity

        grand_total = cart.cart_subtotal+cart.cart_tax+cart.cart_gift_charge
        if grand_total >= 500:
            delivery_charge = 0
        else:
            delivery_charge = 50
        cart.cart_delivery_charge = delivery_charge

        is_coupon_code_valid = False
        if request.method == 'POST':
            coupon_code = request.POST['coupon_code']
            if coupon_code in coupon_codes:
                is_coupon_code_valid = True
                discount_value = coupon_codes[coupon_code]
        cart.cart_discount = discount_value * cart.cart_subtotal
        cart.cart_grand_total = cart.cart_subtotal+cart.cart_tax + \
            cart.cart_gift_charge+cart.cart_delivery_charge - cart.cart_discount
        cart.save()
        context = {"total": cart.cart_subtotal, 'quantity': quantity, 'cart_items': cart_items, 'tax': cart.cart_tax,
                   'delivery_charge': cart.cart_delivery_charge, 'grand_total': cart.cart_grand_total, 'gift_charge': cart.cart_gift_charge, 'discount': cart.cart_discount,
                   'is_coupon_code_valid': is_coupon_code_valid}
    except ObjectDoesNotExist:
        pass
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    except ObjectDoesNotExist:
        pass
    context = {"total": cart.cart_subtotal, 'quantity': quantity, 'cart_items': cart_items, 'tax': cart.cart_tax,
               'delivery_charge': cart.cart_delivery_charge, 'grand_total': cart.cart_grand_total, 'gift_charge': cart.cart_gift_charge, 'discount': cart.cart_discount}
    return render(request, 'store/checkout.html', context)
