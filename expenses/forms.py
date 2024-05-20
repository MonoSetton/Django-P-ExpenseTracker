from django.forms import ModelForm
from .models import Expense, Category
from django import forms
import datetime


class ExpenseCreationForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )

    class Meta:
        model = Expense
        fields = ['name', 'date', 'amount', 'category']


class CategoryCreationForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
