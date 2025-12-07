from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Product, Order

class IndexView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'featured_products'
    
    def get_queryset(self):
        return Product.objects.all()[:8]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_arrivals'] = Product.objects.all().order_by('-created_at')[:8]
        return context

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.all()

class AboutView(TemplateView):
    template_name = 'about.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.exclude(id=self.object.id)[:4]
        return context

class UserView(TemplateView):
    template_name = 'user.html'

class UserSectionView(LoginRequiredMixin, TemplateView):
    template_name = 'userSection.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)[:5]
        return context