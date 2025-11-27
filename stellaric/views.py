from django.shortcuts import render
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, "index.html")

def shop(request):
    return render(request, 'shop.html')

def about(request):
    return render(request, 'about.html')

def product(request):
    return render(request, 'product.html')

def user(request):
    return render(request, 'user.html')

def login(request):
    return render(request, 'login.html')