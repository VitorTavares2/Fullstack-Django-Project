from django.urls import path 
from . import views
from .models import Profile


urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path("profile/", Profile, name="profile"),
    path("update-profile/", views.update_profile, name="update_profile"),
]