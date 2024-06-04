from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, UpdateUsername, UpdateEmail
from django.views.generic import TemplateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_field_name = True
    fields = '__all__'
    success_url = reverse_lazy('expenses')


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('expenses')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('expenses')
        return super(SignupView, self).get(*args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    login_url = '/login/'
    success_url = reverse_lazy('profile')


class UpdateUsernameView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUsername
    template_name = 'accounts/update_username.html'
    login_url = '/login/'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UpdateEmailView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateEmail
    template_name = 'accounts/update_email.html'
    login_url = '/login/'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = '/login/'