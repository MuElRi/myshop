from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/', views.UpdateCartView.as_view(), name='update_cart'),
]

