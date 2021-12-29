
from django.core import mail
from .forms import OrderForm
from cart.models import CartItem
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
# from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
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


def payments(request):
    # return HttpResponse('ok')
    #!Payment gateway code leaving blank
    #!Payment gateway code leaving blank end
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number='2021122940')
    payment = Payment(
        user=request.user,
        payment_id='1234556',
        payment_method='Dummy',
        amount_paid=order.order_total,
        status='Completed'
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.ordered_quantity += item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()
    # mail_subject = 'Thank you for your order!'
    # message = render_to_string(
    #     'order/order-received-email.html', {'user': request.user, 'order': order, 'uid': urlsafe_base64_encode(force_bytes(request.user.pk)), 'token': default_token_generator.make_token(request.user)})

    # subject, from_email, to = 'hello', settings.EMAIL_HOST_USER, request.user.email
    # msg = EmailMultiAlternatives(subject, message, from_email, [to])
    # msg.send()
    data = {'order_number': order.order_number, 'transID': payment.payment_id}
    return redirect('cart')
    # return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    # tax = (2 * total)/100
    grand_total = total + tax
    if grand_total >= 500:
        delivery_charge = 0
    else:
        delivery_charge = 50
    grand_total = total + tax + delivery_charge
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
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
            data.delivery_charge = delivery_charge
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            print(order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'delivery_charge': delivery_charge,
                'grand_total': grand_total,
            }
            # return redirect('checkout')
            return render(request, 'order/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    #*Original code bro
    # order_number = request.GET.get('order_number')
    # transID = request.GET.get('payment_id')
    #*Original code bro

    order_number = '2021122940'
    transID = '1234556'
    print(transID)

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        print('In try block')
        return render(request, 'order/order-complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
