from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("<h1>Hello from index page</h1>")


def about(request):
    return HttpResponse("<h2>this is the About page</h2>")