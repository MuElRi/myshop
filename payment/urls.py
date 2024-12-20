from django.urls import path
from . import views
from .application import webhooks

app_name = 'payment'

urlpatterns = [
    path('process/', views.PaymentProcessView.as_view(), name='process'),
    path('webhook/', webhooks.payment_webhook, name='webhook')
]