from django.shortcuts import render
from datetime import datetime
from .models import Product

# Create your views here.
def products(request):
    context = {
       'products' : Product.objects.all()
    }
    return render(request, "products/products.html", context)


def product(request):
    return render(request, "products/product.html")


def search(request):
    return render(request, "products/search.html")
