from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from account.models import Profile

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError("Passwords don't match.")
#         return cd['password2']
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if email == "" or email is None:
#             raise forms.ValidationError("Email is empty.")
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email already registered.")
#         return email
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#             if hasattr(self, "save_m2m"):
#                 self.save_m2m()
#         return user

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('First name is required.')
        return first_name

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(user=user)
        return user



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return email

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
