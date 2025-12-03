from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from stellaric import views

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('user/', views.user, name='user'),
    path('userSection/', views.userSection, name='userSection'),
    path('auth/', include('users.urls')),  
    path('cart/', include('cart.urls')),
]

# SEMPRE servir media files, mesmo em produção
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)