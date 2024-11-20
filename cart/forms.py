from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices = PRODUCT_QUANTITY_CHOICES, coerce = int, required=False)
    action_type = forms.CharField(widget=forms.HiddenInput())
    product_id = forms.IntegerField(widget=forms.HiddenInput())