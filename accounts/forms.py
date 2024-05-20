from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUsername(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username']


class UpdateEmail(UserChangeForm):
    email = forms.EmailField(required=True)
    password = None

    class Meta:
        model = User
        fields = ['email']

