from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, 'user.html') 
    else:
        Firstname = request.POST.get('Firstname')
        Lastname = request.POST.get('Lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = username).first()
        
        if user:
            return render(request, 'login.html')

        user = User.objects.create_user(first_name = Firstname,last_name = Lastname, username = username, email = email, password = password)
        user.save()
        return HttpResponse('Usuário cadastrado')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password  = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login_django(request, user)
            return HttpResponse('authenticated')
        else:
            return HttpResponse('wrong email or password')

def cart(request):
    if request.user.is_authenticated:
        return render(request,'cart.html')
    else:
       return HttpResponse('you need to be logged to acess this page')