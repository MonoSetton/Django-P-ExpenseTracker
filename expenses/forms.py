from django.forms import ModelForm
from .models import Expense, Category, Budget
from django import forms
import datetime
from django.contrib.auth.models import User


class ExpenseForm(ModelForm):
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


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'budget']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(author=user)


class BudgetForm(ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Budget
        fields = ['name', 'amount_to_spend', 'start_date', 'end_date']
