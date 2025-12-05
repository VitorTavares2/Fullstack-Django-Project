from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Product, Cart, CartItem, Order, OrderItem

import uuid  # used to generate fake payment IDs


# ---------------------------------------------------------------------
# CART
# ---------------------------------------------------------------------

@login_required
def cart_view(request):
    """
    Display the user's cart with subtotal, discount, and total.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    subtotal = cart.get_total()
    discount = Decimal('0')
    
    # Check if a coupon was applied
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
    """
    Add a product to the user's cart with the selected size and quantity.
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', '')
        
        # If the item exists, update quantity. Otherwise, create a new one.
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
    """
    Remove a specific item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required
def update_cart_item(request, item_id):
    """
    Update the quantity of an existing cart item.
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        # If quantity is valid, update. Otherwise, delete item.
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')


# ---------------------------------------------------------------------
# COUPON
# ---------------------------------------------------------------------

@login_required
def apply_coupon(request):
    """
    Apply a discount coupon to the cart.
    """
    if request.method == 'POST':
        coupon = request.POST.get('coupon', '').strip().upper()
        
        if coupon == 'STELLA15':
            request.session['coupon_applied'] = True
            messages.success(request, 'Coupon applied successfully! 15% discount')
        else:
            messages.warning(request, 'Invalid coupon code')
            request.session['coupon_applied'] = False
    
    return redirect('cart')


# ---------------------------------------------------------------------
# CHECKOUT
# ---------------------------------------------------------------------

@login_required
def checkout(request):
    """
    Display checkout page with summarized cart information.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

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

    return render(request, 'checkout.html', context)


# ---------------------------------------------------------------------
# CREATE ORDER
# ---------------------------------------------------------------------

@login_required
def create_order(request):
    """
    Create an order from the user's cart and redirect to payment page.
    """
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Check if user's address is complete
    if not (
        request.user.profile.Adress and 
        request.user.profile.City and
        request.user.profile.ZIPCODE and 
        request.user.profile.State
    ):
        messages.warning(request, 'Your address is not valid!')
        return redirect('userSection')

    subtotal = cart.get_total()
    discount = Decimal('0')

    if request.session.get('coupon_applied'):
        discount = subtotal * Decimal('0.15')

    final_amount = subtotal - discount

    # Create the order
    order = Order.objects.create(
        user=request.user,
        order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        total_amount=subtotal,
        discount=discount,
        final_amount=final_amount,
        shipping_adress=request.user.profile.Adress,
        shipping_city=request.user.profile.City,
        shipping_zipcode=request.user.profile.ZIPCODE,
        shipping_state=request.user.profile.State,
    )

    # Transfer cart items into order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            size=item.size,
            price=item.product.price
        )

    # Clear cart
    cart_items.delete()
    request.session['coupon_applied'] = False

    return redirect('payment_page', order_id=order.id)


# ---------------------------------------------------------------------
# FAKE PAYMENT (always approved)
# ---------------------------------------------------------------------

@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "payment.html", {"order": order})


@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method != "POST":
        messages.error(request, "Invalid payment request.")
        return redirect("payment", order_id=order.id)

    order.status = "processing"
    order.payment_id = f"FAKE-{uuid.uuid4().hex[:10].upper()}"
    order.payment_method = "Payment Gateway"
    order.save()

    messages.success(request, f"Payment approved! Order {order.order_number} is now paid.")

    return redirect('order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})