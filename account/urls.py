from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]

