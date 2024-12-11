from django.db import models
from django.conf import settings

class UserCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    items = models.JSONField(default=dict)  # Хранение данных корзины в виде JSON
