from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from stellaric import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Allauth
    path('accounts/', include('allauth.urls')),
    
    # Stellaric
    path('', views.IndexView.as_view(), name='index'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('user/', views.UserView.as_view(), name='user'),
    path('userSection/', views.UserSectionView.as_view(), name='userSection'),
    
    # Users
    path('auth/', include('users.urls')),
    
    # Cart
    path('cart/', include('cart.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)