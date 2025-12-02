from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Product, Cart, CartItem

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    subtotal = cart.get_total()
    discount = Decimal('0')
    
    if request.session.get('coupon_applied'):
        discount = subtotal * Decimal('0.15')
    
    total = subtotal - discount
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', '')
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        return redirect('cart')
    
    return redirect('shop')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')

@login_required
def apply_coupon(request):
    if request.method == 'POST':
        coupon = request.POST.get('coupon', '').strip().upper()
        
        if coupon == 'STELLA15':
            request.session['coupon_applied'] = True
            messages.success(request, 'Coupon applied successfully! 15% discount')
        else:
            messages.warning(request, 'Invalid coupon code')
            request.session['coupon_applied'] = False
    
    return redirect('cart')