from django.forms import ModelForm
from .models import Expense, Category, Budget, BudgetCategory, BudgetExpense
from django import forms
import datetime
from django.contrib.auth.models import User
from django.db.models import Subquery


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
        fields = ['name']


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


class BudgetCategoryForm(ModelForm):
    class Meta:
        model = BudgetCategory
        fields = ['category', 'value']


class BudgetExpenseForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )

    class Meta:
        model = BudgetExpense
        fields = ['name', 'date', 'amount', 'category']

    def __init__(self, *args, **kwargs):
        budget = kwargs.pop('budget', None)
        super().__init__(*args, **kwargs)
        if budget is not None:
            self.fields['category'].queryset = BudgetCategory.objects.filter(budget=budget)
