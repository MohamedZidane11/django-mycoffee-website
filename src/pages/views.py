from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
# Create your views here.


def index(request):
    # return HttpResponse("<h1>Hello from index page</h1>")
    context = {
       'products' : Product.objects.all()
    }
    return render(request, "pages/index.html", context)


def about(request):
    # return HttpResponse("<h2>this is the About page</h2>")
    return render(request, "pages/about.html")


def coffee(request):
    return render(request, "pages/coffee.html")