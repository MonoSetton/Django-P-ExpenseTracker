from django.forms import ModelForm
from .models import Expense, Category
from django import forms
import datetime
from django.contrib.auth.models import User


class ExpenseCreationForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )

    class Meta:
        model = Expense
        fields = ['name', 'date', 'amount', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        admin_users = User.objects.filter(is_superuser=True)
        self.fields['category'].queryset = Category.objects.filter(author__in=[user, *admin_users])


class ExpenseUpdateForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )

    class Meta:
        model = Expense
        fields = ['name', 'date', 'amount', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        admin_users = User.objects.filter(is_superuser=True)
        self.fields['category'].queryset = Category.objects.filter(author__in=[user, *admin_users])


class CategoryCreationForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
