from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Product

# Create your views here.
def products(request):
    context = {
       'products': Product.objects.all()
    }
    return render(request, "products/products.html", context)


def product(request, pro_id):
    context = {
        'pro': get_object_or_404(Product, pk=pro_id)
    }
    return render(request, "products/product.html", context)


def search(request):
    return render(request, "products/search.html")
