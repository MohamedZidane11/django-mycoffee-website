from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import Order
from .models import OrderDetails
from .models import Payment
from django.utils import timezone

# Create your views here.
def add_to_cart(request):

    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET\
    and request.user.is_authenticated and not request.user.is_anonymous:

        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        order =Order.objects.all().filter(user=request.user, is_finished=False)

        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products:products')

        pro = Product.objects.get(id=pro_id)

        if order:
            #messages.warning(request, 'يوجد طلب قديم')
            old_order = Order.objects.get(user=request.user, is_finished=False)
            if OrderDetails.objects.all().filter(order=old_order, product=pro).exists():
                orderdetails = OrderDetails.objects.get(order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else:
                orderdetails = OrderDetails.objects.create(product=pro, order=old_order, price=pro.price, quantity=qty)
            messages.success(request, 'Was added to cart for old order')
        else:
            #messages.info(request, 'سوف يتم عمل طلب جديد')
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            orderdetails = OrderDetails.objects.create(product=pro, order=new_order, price=pro.price, quantity=qty)
            messages.success(request, 'Was added to cart for new order')

        return redirect('/products/' + request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request, 'You must be logged in')
            return redirect('/products/' + request.GET['pro_id'])
        else:
            return redirect('pages:index')


def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for sub in orderdetails:
                total += sub.price * sub.quantity
            context = {
                'order': order,
                'orderdetails': orderdetails,
                'total': total,
            }

    return render(request, 'orders/cart.html', context)


def remove_from_cart(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.delete()
    return redirect('orders:cart')


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.quantity += 1
        orderdetails.save()
    return redirect('orders:cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()
    return redirect('orders:cart')


def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    expire = None
    security_code = None
    is_added = None

    if request.method == 'POST' and 'btnpayment' in request.POST and 'ship_address' in request.POST and \
            'ship_phone' in request.POST and 'card_number' in request.POST and 'expire' in request.POST and \
            'security_code' in request.POST:
        # Here Payment process after pressing 'Payment' button
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        expire = request.POST['expire']
        security_code = request.POST['security_code']

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                payment = Payment(order=order, shipment_address=ship_address, shipment_phone=ship_phone,
                                  card_number=card_number, expire=expire, security_code=security_code)
                payment.save()
                order.is_finished = True
                order.save()
                is_added = True
                messages.success(request, 'Your Order is finished')

        context = {
            'ship_address': ship_address,
            'ship_phone': ship_phone,
            'card_number': card_number,
            'expire': expire,
            'security_code': security_code,
            'is_added': is_added,
        }
        pass
    else:
        # Here Display details before pressing 'Payment' button
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for sub in orderdetails:
                    total += sub.price * sub.quantity

                context = {
                    'order': order,
                    'orderdetails': orderdetails,
                    'total': total,
                }

    return render(request, 'orders/payment.html', context)
