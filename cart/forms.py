from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    product_id = forms.IntegerField(widget=forms.HiddenInput())