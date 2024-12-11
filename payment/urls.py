from django.urls import path
from . import views
from .application import webhooks

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('webhook/', webhooks.payment_webhook, name='webhook')
]