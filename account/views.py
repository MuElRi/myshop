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



# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             return render(request, 'account/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request,
#                     'account/register.html',
#                     {'user_form': user_form})

# @login_required
# def edit(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user, data=request.POST)
#         profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Profile updated successfully')
#         else:
#             messages.error(request, 'Error updating your profile')
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = ProfileEditForm(instance=request.user.profile)
#
#     return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

# @login_required
# def profile(request):
#     return render(request, 'account/profile.html')













