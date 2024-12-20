from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/done', views.RegisterDoneView.as_view(), name='register_done'),
    path('edit/', views.EditProfileView.as_view(), name='edit'),
]

