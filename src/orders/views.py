from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
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
        return redirect('products:products')


def cart(request):
    return render(request, 'orders/cart.html')
