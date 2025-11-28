from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib import messages

def register(request):
    if request.method == "GET":
        return render(request, 'user.html')
    
    Firstname = request.POST.get('Firstname')
    Lastname = request.POST.get('Lastname')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = User.objects.filter(username=username).first()

    if user:
        messages.error(request, "Username already exists!")
        return redirect("login")

    user = User.objects.create_user(
        first_name=Firstname,
        last_name=Lastname,
        username=username,
        email=email,
        password=password
    )
    user.save()

    messages.success(request, "Registered user successfully!")
    return redirect("login")


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user:
        login_django(request, user)
        messages.success(request, "Authenticated!")
        return redirect("index")
    else:
        messages.warning(request, "Wrong email or password!")
        return redirect("login")


def cart(request):
    if request.user.is_authenticated:
        return render(request, 'cart.html')
    
    messages.warning(request, "You need to be logged in to access this page!")
    return redirect("register")
