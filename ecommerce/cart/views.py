from django.shortcuts import render, HttpResponse, redirect
from shop.models import Product
from .models import Cart, Order_table
from django.contrib.auth.decorators import login_required
import razorpay
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login


@login_required
def add_to_cart(request, i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (p.stock > 0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if (p.stock):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart_view')


@login_required
def cart_view(request):
    u = request.user
    cart = Cart.objects.filter(user=u)
    total = 0
    for i in cart:
        total = total + i.quantity * i.product.price

    return render(request, 'cart.html', {'cart': cart, 'total': total})


@login_required
def cart_remove(request, i, c_id):
    user = request.user
    p = Product.objects.get(id=i)
    cart = Cart.objects.get(user=user, product=p)
    q = cart.quantity

    cart.quantity -= cart.quantity
    cart.save()

    p.stock += q
    p.save()

    c = Cart.objects.get(id=c_id)
    c.delete()
    return redirect('cart:cart_view')


@login_required
def decrement(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cart_view')


# def cart_remove(request,i):
#     p = Product.objects.get(id=i)
#     u = request.user
#     try:
#         cart = Cart.objects.get(user=u, product=p)
#         cart.delete()
#         p.stock += cart.quantity
#         p.save()
#     except:
#         pass
#     return redirect('cart:viewcart')
@login_required
def place_order(request):
    if (request.method == "POST"):
        ph = request.POST.get('ph')
        a = request.POST.get('a')
        pin = request.POST.get('pin')
        u = request.user
        c = Cart.objects.filter(user=u)

        total = 0
        for i in c:
            total = (total + (i.quantity * i.product.price))
        total = int(total * 100)

        client = razorpay.Client(auth=('rzp_test_exAlWd6fwlr3BO', 'GZTfRsKfRon1EDgYk3L54sEf'))
        response_payment = client.order.create(dict(amount=total, currency="INR"))
        print(response_payment)

        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == 'created':
            p = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()

            for i in c:
                o = Order_table.objects.create(user=u, product=i.product, address=a, phone=ph, pin=pin,
                                               no_of_items=i.quantity, order_id=order_id)
                o.save()
        response_payment['name'] = u.username
        return render(request, 'payment.html', {'payment': response_payment})

    return render(request, 'place_order.html')


@csrf_exempt
def payment_status(request, u):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        u = User.objects.get(username=u)
        login(request,u)
        print(request.user.is_authenticated)


    if (request.method == 'POST'):
        response = request.POST
        # print(response)
        # print(u)
        param_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_exAlWd6fwlr3BO', 'GZTfRsKfRon1EDgYk3L54sEf'))
        try:
            status = client.utility.verify_payment_signature(param_dict)
            print(status)

            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id']
            ord.paid = True
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)
            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="paid"
                i.save()
            c.delete()
            return render(request,'payment_status.html',{'status':True})

        except:
            return render(request, 'payment_status.html', {'status': False})

    return render(request, 'payment_status.html')

@login_required
def order_details(request):
    u=request.user
    customer=Order_table.objects.filter(user=u,payment_status='paid')
    return render(request,'order_details.html',{'orders':customer,'u':u})