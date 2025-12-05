from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Product

def index(request):
    featured_products = Product.objects.all()[:8]
    new_arrivals = Product.objects.all().order_by('-created_at')[:8]
    
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals
    }
    return render(request, "index.html", context)

def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop.html', context)

def about(request):
    return render(request, 'about.html')

def product(request):
    return render(request, 'product.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.exclude(id=product_id)[:4]
    context = {
        'product': product,
        'products': products
    }
    return render(request, 'product.html', context)

def user(request):
    return render(request, 'user.html')

def login(request):
    return render(request, 'login.html')

def userSection(request):
    if request.user.is_authenticated:
        return render(request, 'userSection.html')
    else:
        return redirect('register')

def checkout(request):
    return render(request, 'checkout.html')