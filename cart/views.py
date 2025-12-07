from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
import uuid
import random

from .models import Product, Cart, CartItem, Order, OrderItem


# ---------------------------------------------------------------------
# CART
# ---------------------------------------------------------------------

class CartView(LoginRequiredMixin, TemplateView):
    """
    Display the user's cart with subtotal, discount, and total.
    """
    template_name = 'cart.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_items = cart.items.all()
        
        subtotal = cart.get_total()
        discount = Decimal('0')
        
        if self.request.session.get('coupon_applied'):
            discount = subtotal * Decimal('0.15')
        
        total = subtotal - discount
        
        context['cart_items'] = cart_items
        context['subtotal'] = subtotal
        context['discount'] = discount
        context['total'] = total
        
        return context


class AddToCartView(LoginRequiredMixin, View):
    """
    Add a product to the user's cart with the selected size and quantity.
    """
    login_url = 'account_login'
    
    def post(self, request, product_id):
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
    
    def get(self, request, product_id):
        return redirect('shop')


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Remove a specific item from the cart.
    """
    login_url = 'account_login'
    
    def get(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
        return redirect('cart')


class UpdateCartItemView(LoginRequiredMixin, View):
    """
    Update the quantity of an existing cart item.
    """
    login_url = 'account_login'
    
    def post(self, request, item_id):
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


# ---------------------------------------------------------------------
# COUPON
# ---------------------------------------------------------------------

class ApplyCouponView(LoginRequiredMixin, View):
    """
    Apply a discount coupon to the cart.
    """
    login_url = 'account_login'
    
    def post(self, request):
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

class CheckoutView(LoginRequiredMixin, TemplateView):
    """
    Display checkout page with summarized cart information.
    """
    template_name = 'checkout.html'
    login_url = 'account_login'
    
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        if not cart_items:
            messages.warning(request, 'Your cart is empty!')
            return redirect('cart')
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = cart.items.all()

        subtotal = cart.get_total()
        discount = Decimal('0')

        if self.request.session.get('coupon_applied'):
            discount = subtotal * Decimal('0.15')
        
        total = subtotal - discount

        context['cart_items'] = cart_items
        context['subtotal'] = subtotal
        context['discount'] = discount
        context['total'] = total
        
        return context


# ---------------------------------------------------------------------
# CREATE ORDER
# ---------------------------------------------------------------------

class CreateOrderView(LoginRequiredMixin, View):
    """
    Create an order from the user's cart and redirect to payment page.
    """
    login_url = 'account_login'
    
    def post(self, request):
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
            shipping_address=request.user.profile.Adress,
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
    
    def get(self, request):
        return redirect('checkout')


# ---------------------------------------------------------------------
# FAKE PAYMENT (always approved)
# ---------------------------------------------------------------------

class PaymentPageView(LoginRequiredMixin, DetailView):
    """
    Display payment page for a specific order.
    """
    model = Order
    template_name = 'payment.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    login_url = 'account_login'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class ProcessPaymentView(LoginRequiredMixin, View):
    """
    Process fake payment and mark order as paid.
    """
    login_url = 'account_login'
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        order.status = "processing"
        order.payment_id = f"FAKE-{uuid.uuid4().hex[:10].upper()}"
        order.payment_method = "Payment Gateway"
        order.save()

        messages.success(request, f"Payment approved! Order {order.order_number} is now paid.")

        return redirect('order_detail', order_id=order.id)
    
    def get(self, request, order_id):
        messages.error(request, "Invalid payment request.")
        return redirect('payment_page', order_id=order_id)


# ---------------------------------------------------------------------
# ORDER MANAGEMENT
# ---------------------------------------------------------------------

class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information about a specific order.
    """
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    login_url = 'account_login'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderHistoryView(LoginRequiredMixin, ListView):
    """
    Display all orders for the current user.
    """
    model = Order
    template_name = 'order_history.html'
    context_object_name = 'orders'
    login_url = 'account_login'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)