from django.shortcuts import render, redirect

# Create your views here.
def add_to_cart(request):
    return redirect('products')
