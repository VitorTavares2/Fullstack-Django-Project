from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib import messages
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from .models import Profile

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

def logout(request):
    logout_django(request)
    messages.success(request, "Logged out successfully!")
    return redirect("index")

def Profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.address = request.POST.get("address")
        profile.city = request.POST.get("city")
        profile.state = request.POST.get("state")
        profile.zipcode = request.POST.get("zipcode")
        profile.phone = request.POST.get("phone")
        profile.save()

        messages.success(request, "Profile updated.")
        return redirect("profile")

    return render(request, "profile.html", {"profile": profile})

def update_profile(request):
    if request.method == "POST":
        profile = request.user.profile 

        # Update fields with the EXACT names from the HTML form
        profile.phone = request.POST.get("phone")
        profile.Adress = request.POST.get("Adress")  
        profile.ZIPCODE = request.POST.get("ZIPCODE") 
        profile.City = request.POST.get("City")  
        profile.State = request.POST.get("State") 

        profile.save()  

        messages.success(request, "Profile updated successfully!")
        return redirect("userSection")  

    return redirect("userSection")  