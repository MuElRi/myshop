from dataclasses import fields

from django import forms
from .models import Order

# class OrderCreateForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['city', 'email', 'postal_code', 'street', 'house_number', 'apartment_number']

OrderCreateForm = forms.modelform_factory(
    Order,
    fields = [
        'city', 'email',
        'postal_code', 'street',
        'house_number', 'apartment_number'
    ]
)
