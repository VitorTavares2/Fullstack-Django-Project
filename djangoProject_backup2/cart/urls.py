from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('coupon/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    path('payment/<int:order_id>/', views.PaymentPageView.as_view(), name='payment_page'),
    path('process-payment/<int:order_id>/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('order/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
]