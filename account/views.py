from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import commit
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'


class EditProfileView(LoginRequiredMixin, FormView):
    user_form_class = UserEditForm
    profile_form_class = ProfileEditForm
    template_name = 'account/edit.html'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class(
            instance=self.request.user)
        profile_form = self.profile_form_class(
            instance=self.request.user.profile)
        return render(self.request, self.template_name,
                    {'user_form': user_form,
                            'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=self.request.user,
                                 data=self.request.POST)
        profile_form = ProfileEditForm(instance=self.request.user.profile,
                                       data=self.request.POST,
                                       files=self.request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form=user_form,
                                   profile_form=profile_form)
        else:
            return self.form_invalid(user_form=user_form,
                                     profile_form=profile_form)

    def form_valid(self, **kwargs):
        kwargs['user_form'].save()
        kwargs['profile_form'].save()
        messages.success(self.request, 'Profile updated successfully')
        return render(self.request, self.template_name, kwargs)

    def form_invalid(self, **kwargs):
        messages.error(self.request, 'Error updating your profile')
        return render(self.request, self.template_name, **kwargs)


class RegisterDoneView(TemplateView):
    template_name = 'account/register_done.html'


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('register_done')

















