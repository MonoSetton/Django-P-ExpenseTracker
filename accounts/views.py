from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UpdateUsername, UpdateEmail, ChangePasswordForm
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request=request)
        if form.is_valid():
            newpassword = form.cleaned_data['newpassword1']
            username = request.user.username
            password = form.cleaned_data['oldpassword']

            user = authenticate(username=username, password=password)
            user.set_password(newpassword)
            user.save()
            return redirect('/')
    else:
        form = ChangePasswordForm()
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='/login')
def update_username(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateUsername(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = UpdateUsername()

    return render(request, 'accounts/update_username.html', {'form': form})


@login_required(login_url='/login')
def update_email(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateEmail(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = UpdateEmail()

    return render(request, 'accounts/update_email.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = 'login/'