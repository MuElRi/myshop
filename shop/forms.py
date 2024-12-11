from django import forms

class PriceFilterForm(forms.Form):
    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'От'})
    )
    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'До'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        if min_price is not None and max_price is not None:
            if max_price < min_price:
                # cleaned_data['min_price'], cleaned_data['max_price'] = max_price, min_price
                raise forms.ValidationError("Invalid value")
        return cleaned_data

    def clean_max_price(self):
        max_price = self.cleaned_data['max_price']
        if max_price is not None:
            if max_price < 0:
                # max_price = abs(max_price)
                raise forms.ValidationError("Invalid value")
        return max_price

