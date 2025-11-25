from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def shop(request):
    return render(request, 'shop.html')

def about(request):
    return render(request, 'about.html')

def product(request):
    return render(request, 'product.html')

def cart(request):
    return render(request, 'cart.html')

def user(request):
    return render(request, 'user.html')

def login(request):
    return render(request, 'login.html')