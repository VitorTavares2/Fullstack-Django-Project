from django.contrib import admin
from django.urls import path,include
from stellaric import views
from users import views as viewsUsers

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('product/', views.product, name='product'),
    path('cart/', viewsUsers.cart, name='cart'),
    path('user/', views.user, name='user'),
    path('login/', views.login, name='login'),
    path('auth/', include('users.urls')),
]
