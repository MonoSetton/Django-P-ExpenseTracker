from django.test import TestCase
from django.contrib.auth.models import User
from .forms import ExpenseForm, CategoryForm, BudgetForm, BudgetCategoryForm, BudgetExpenseForm
from .models import Category, Budget, BudgetCategory
import datetime


class ExpenseFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category', author=self.user)

    def test_expense_form_valid(self):
        form_data = {
            'name': 'Test Expense',
            'date': datetime.date.today(),
            'amount': 100,
            'category': self.category.id,
        }
        form = ExpenseForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_expense_form_invalid(self):
        form_data = {
            'name': '',
            'date': datetime.date.today(),
            'amount': 100,
            'category': self.category.id,
        }
        form = ExpenseForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())


class CategoryFormTest(TestCase):

    def test_category_form_valid(self):
        form_data = {
            'name': 'Test Category',
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        form_data = {
            'name': '',
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())


class BudgetFormTest(TestCase):

    def test_budget_form_valid(self):
        form_data = {
            'name': 'Test Budget',
            'amount_to_spend': 1000,
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today() + datetime.timedelta(days=30),
        }
        form = BudgetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_budget_form_invalid(self):
        form_data = {
            'name': '',
            'amount_to_spend': -1000,
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today() - datetime.timedelta(days=30),
        }
        form = BudgetForm(data=form_data)
        self.assertFalse(form.is_valid())


class BudgetCategoryFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category', author=self.user)
        self.budget = Budget.objects.create(name='Test Budget', amount_to_spend=1000, start_date=datetime.date.today(), end_date=datetime.date.today() + datetime.timedelta(days=30), author=self.user)

    def test_budget_category_form_valid(self):
        form_data = {
            'category': self.category.id,
            'value': 500,
        }
        form = BudgetCategoryForm(data=form_data, budget=self.budget)
        self.assertTrue(form.is_valid())

    def test_budget_category_form_invalid(self):
        form_data = {
            'category': self.category.id,
            'value': 'invalid',
        }
        form = BudgetCategoryForm(data=form_data, budget=self.budget)
        self.assertFalse(form.is_valid())


class BudgetExpenseFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category', author=self.user)
        self.budget = Budget.objects.create(name='Test Budget', amount_to_spend=1000, start_date=datetime.date.today(), end_date=datetime.date.today() + datetime.timedelta(days=30), author=self.user)
        self.budget_category = BudgetCategory.objects.create(budget=self.budget, category=self.category, value=500)

    def test_budget_expense_form_valid(self):
        form_data = {
            'name': 'Test Expense',
            'date': datetime.date.today(),
            'amount': 100,
            'category': self.budget_category.id,
        }
        form = BudgetExpenseForm(data=form_data, budget=self.budget)
        self.assertTrue(form.is_valid())

    def test_budget_expense_form_invalid(self):
        form_data = {
            'name': '',
            'date': datetime.date.today(),
            'amount': -100,
            'category': self.budget_category.id,
        }
        form = BudgetExpenseForm(data=form_data, budget=self.budget)
        self.assertFalse(form.is_valid())
