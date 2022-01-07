
from django.core import mail
from .forms import OrderForm
from cart.models import CartItem, Cart
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
# from .forms import OrderForm
import datetime
from .models import Order, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from cart.views import _get_cart_id

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# def payments(request):
#     pass


def place_order(request, quantity=0, total=0):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pin = form.cleaned_data['pin']
            data.order_note = form.cleaned_data['order_note']
            data.delivery_charge = cart.cart_delivery_charge
            data.gift_charge = cart.cart_gift_charge
            data.discount = cart.cart_discount
            data.order_total = cart.cart_grand_total
            data.tax = cart.cart_tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            currency = 'INR'
            razorpay_amount = cart.cart_grand_total*100  # Rs. 200

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=razorpay_amount,
                                                               currency=currency,
                                                               payment_capture='0'))

            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            data.order_number = razorpay_order_id
            data.save()
            order = Order.objects.get(
                user=request.user, is_ordered=False, order_number=data.order_number)
            callback_url = 'paymenthandler/'
            razorpay_merchant_key = settings.RAZOR_KEY_ID
            # we need to pass these details to frontend.
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': cart.cart_subtotal,
                'tax': cart.cart_tax,
                'delivery_charge': cart.cart_delivery_charge,
                'gift_charge': cart.cart_gift_charge,
                'discount': cart.cart_discount,
                'grand_total': cart.cart_grand_total,
                'razorpay_order_id': razorpay_order_id,
                'currency': currency,
                'callback_url': callback_url,
            }

            return render(request, 'order/payments.html', context)
    else:
        return redirect('checkout')


# regarding Razorpay

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            if result is None:
                amount = cart.cart_grand_total*100
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    order = Order.objects.get(
                        order_number=razorpay_order_id, user=request.user)
                    order.is_ordered = True
                    order.transID = payment_id
                    order.save()
                    ordered_products = OrderProduct.objects.filter(
                        order_id=order.id)
                    cart_items = CartItem.objects.filter(user=request.user)
                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.user_id = request.user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.ordered = True
                        orderproduct.save()
                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variations.all()
                        orderproduct = OrderProduct.objects.get(
                            id=orderproduct.id)
                        orderproduct.variations.set(product_variation)
                        orderproduct.save()

                        # Reduce the quantity of the sold products and increase the quantity of order products
                        product = Product.objects.get(id=item.product_id)
                        product.stock -= item.quantity
                        product.ordered_quantity += item.quantity
                        product.popularity += item.quantity
                        product.save()

                    CartItem.objects.filter(user=request.user).delete()
                    cart.delete()
                    subtotal = 0
                    for i in ordered_products:
                        subtotal += i.product_price * i.quantity
                    context = {
                        'order': order,
                        'ordered_products': ordered_products,
                        'order_number': order.order_number,
                        'transID': order.transID,
                        'subtotal': subtotal,
                    }
                    # render success page on successful capture of payment
                    return render(request, 'order/order-complete.html', context)
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
