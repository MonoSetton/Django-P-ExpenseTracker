from django.test import TestCase
from django.contrib.auth.models import User
from .forms import ExpenseForm, CategoryForm, BudgetForm, BudgetCategoryForm, BudgetExpenseForm
from .models import Category, Budget, BudgetCategory, Expense, BudgetExpense
from django.utils import timezone
import datetime
from django.urls import reverse, resolve
from django.db.models import Sum
from decimal import Decimal
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from expenses import views


class ExpensesUrlsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@example.com',
                                             password='password123')
        self.token = default_token_generator.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

        self.expenses_url = reverse('expenses')
        self.create_expense_url = reverse('create_expense')
        self.update_expense_url = reverse('update_expense', args=['1'])
        self.delete_expense_url = reverse('delete_expense', args=['1'])
        self.create_category_url = reverse('create_category')
        self.update_category_url = reverse('update_category', args=['1'])
        self.delete_category_url = reverse('delete_category', args=['1'])
        self.list_categories_url = reverse('list_categories')
        self.budgets_url = reverse('budgets')
        self.budget_details_url = reverse('budget_details', args=['1'])
        self.create_budget_url = reverse('create_budget')
        self.update_budget_url = reverse('update_budget', args=['1'])
        self.delete_budget_url = reverse('delete_budget', args=['1'])
        self.add_category_to_budget_url = reverse('add_category_to_budget', args=['1'])
        self.delete_category_from_budget_url = reverse('delete_category_from_budget', args=['1'])
        self.add_expense_to_budget_url = reverse('add_expense_to_budget', args=['1'])
        self.update_budget_expense_url = reverse('update_budget_expense', args=['1'])
        self.delete_budget_expense_url = reverse('delete_budget_expense', args=['1'])

    def test_expenses_url(self):
        self.assertEqual(resolve(self.expenses_url).func.view_class, views.ExpensesView)

    def test_create_expense_url(self):
        self.assertEqual(resolve(self.create_expense_url).func.view_class, views.CreateExpenseView)

    def test_update_expense_url(self):
        self.assertEqual(resolve(self.update_expense_url).func.view_class, views.UpdateExpenseView)

    def test_delete_expense_url(self):
        self.assertEqual(resolve(self.delete_expense_url).func.view_class, views.DeleteExpenseView)

    def test_create_category_url(self):
        self.assertEqual(resolve(self.create_category_url).func.view_class, views.CreateCategoryView)

    def test_update_category_url(self):
        self.assertEqual(resolve(self.update_category_url).func.view_class, views.UpdateCategoryView)

    def test_delete_category_url(self):
        self.assertEqual(resolve(self.delete_category_url).func.view_class, views.DeleteCategoryView)

    def test_list_categories_url(self):
        self.assertEqual(resolve(self.list_categories_url).func.view_class, views.CategoryListView)

    def test_budgets_url(self):
        self.assertEqual(resolve(self.budgets_url).func.view_class, views.BudgetView)

    def test_budget_details_url(self):
        self.assertEqual(resolve(self.budget_details_url).func.view_class, views.DetailsBudgetView)

    def test_create_budget_url(self):
        self.assertEqual(resolve(self.create_budget_url).func.view_class, views.CreateBudgetView)

    def test_update_budget_url(self):
        self.assertEqual(resolve(self.update_budget_url).func.view_class, views.UpdateBudgetView)

    def test_delete_budget_url(self):
        self.assertEqual(resolve(self.delete_budget_url).func.view_class, views.DeleteBudgetView)

    def test_add_category_to_budget_url(self):
        self.assertEqual(resolve(self.add_category_to_budget_url).func.view_class, views.AddCategoryToBudget)

    def test_delete_category_from_budget_url(self):
        self.assertEqual(resolve(self.delete_category_from_budget_url).func.view_class, views.DeleteCategoryFromBudget)

    def test_add_expense_to_budget_url(self):
        self.assertEqual(resolve(self.add_expense_to_budget_url).func.view_class, views.CreateBudgetExpenseView)

    def test_update_budget_expense_url(self):
        self.assertEqual(resolve(self.update_budget_expense_url).func.view_class, views.UpdateBudgetExpenseView)

    def test_delete_budget_expense_url(self):
        self.assertEqual(resolve(self.delete_budget_expense_url).func.view_class, views.DeleteBudgetExpenseView)


# class ExpenseFormTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.category = Category.objects.create(name='Test Category', author=self.user)
#         self.category_2 = Category.objects.create(name='Test Category 2', author=self.user)
#         self.budget = Budget.objects.create(name='Test Budget', amount_to_spend=1000, start_date=datetime.date.today(), end_date=datetime.date.today() + datetime.timedelta(days=30), author=self.user)
#         self.budget_category = BudgetCategory.objects.create(budget=self.budget, category=self.category, value=500)
#
#     def test_expense_form_valid(self):
#         form_data = {
#             'name': 'Test Expense',
#             'date': datetime.date.today(),
#             'amount': 100,
#             'category': self.category.id,
#         }
#         form = ExpenseForm(data=form_data, user=self.user)
#         self.assertTrue(form.is_valid())
#
#     def test_expense_form_invalid(self):
#         form_data = {
#             'name': '',
#             'date': datetime.date.today(),
#             'amount': 100,
#             'category': self.category.id,
#         }
#         form = ExpenseForm(data=form_data, user=self.user)
#         self.assertFalse(form.is_valid())
#
#     def test_category_form_valid(self):
#         form_data = {
#             'name': 'Test Category',
#         }
#         form = CategoryForm(data=form_data)
#         self.assertTrue(form.is_valid())
#
#     def test_category_form_invalid(self):
#         form_data = {
#             'name': '',
#         }
#         form = CategoryForm(data=form_data)
#         self.assertFalse(form.is_valid())
#
#     def test_budget_form_valid(self):
#         form_data = {
#             'name': 'Test Budget',
#             'amount_to_spend': 1000,
#             'start_date': datetime.date.today(),
#             'end_date': datetime.date.today() + datetime.timedelta(days=30),
#         }
#         form = BudgetForm(data=form_data)
#         self.assertTrue(form.is_valid())
#
#     def test_budget_form_invalid(self):
#         form_data = {
#             'name': '',
#             'amount_to_spend': -1000,
#             'start_date': datetime.date.today(),
#             'end_date': datetime.date.today() - datetime.timedelta(days=30),
#         }
#         form = BudgetForm(data=form_data)
#         self.assertFalse(form.is_valid())
#
#     def test_budget_category_form_valid(self):
#         form_data = {
#             'budget': self.budget,
#             'category': self.category_2.id,
#             'value': 500,
#         }
#         form = BudgetCategoryForm(data=form_data, budget=self.budget)
#         self.assertTrue(form.is_valid())
#
#     def test_budget_category_form_invalid(self):
#         form_data = {
#             'category': self.category.id,
#             'value': 'invalid',
#         }
#         form = BudgetCategoryForm(data=form_data, budget=self.budget)
#         self.assertFalse(form.is_valid())
#
#     def test_budget_expense_form_valid(self):
#         form_data = {
#             'name': 'Test Expense',
#             'date': datetime.date.today(),
#             'amount': 100,
#             'category': self.budget_category.id,
#         }
#         form = BudgetExpenseForm(data=form_data, budget=self.budget)
#         self.assertTrue(form.is_valid())
#
#     def test_budget_expense_form_invalid(self):
#         form_data = {
#             'name': '',
#             'date': datetime.date.today(),
#             'amount': -100,
#             'category': self.budget_category.id,
#         }
#         form = BudgetExpenseForm(data=form_data, budget=self.budget)
#         self.assertFalse(form.is_valid())
#
#
# class ExpenseViewsTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.category = Category.objects.create(name='Test Category', author=self.user)
#         self.category_budget = Category.objects.create(name='Test Category for Budget', author=self.user)
#         self.budget = Budget.objects.create(
#             name='Test Budget',
#             amount_to_spend=10000,
#             start_date=timezone.now().date(),
#             end_date=timezone.now().date(),
#             author=self.user
#         )
#
#         self.budget_category = BudgetCategory.objects.create(
#             budget=self.budget,
#             category=self.category,
#             value=100.10
#         )
#
#         self.budget.categories.set([self.category])
#
#         self.expense = Expense.objects.create(
#             name='Test Expense',
#             date=timezone.now().date(),
#             amount=10.50,
#             category=self.category,
#             author=self.user
#         )
#
#         self.budget_expense = BudgetExpense.objects.create(
#             name='Test Budget Expense',
#             date=timezone.now().date(),
#             amount=10.50,
#             category=self.budget_category,
#             author=self.user
#         )
#
#         self.expenses_url = reverse('expenses')
#         self.create_expense_url = reverse('create_expense')
#         self.update_expense_url = reverse('update_expense', args=[self.expense.id])
#         self.delete_expense_url = reverse('delete_expense', args=[self.expense.id])
#         self.create_category_url = reverse('create_category')
#         self.update_category_url = reverse('update_category', args=[self.category.id])
#         self.delete_category_url = reverse('delete_category', args=[self.category.id])
#         self.list_categories_url = reverse('list_categories')
#         self.budgets_url = reverse('budgets')
#         self.budget_details_url = reverse('budget_details', args=[self.budget.id])
#         self.create_budget_url = reverse('create_budget')
#         self.update_budget_url = reverse('update_budget', args=[self.budget.id])
#         self.delete_budget_url = reverse('delete_budget', args=[self.budget.id])
#         self.add_category_to_budget_url = reverse('add_category_to_budget', args=[self.budget.id])
#         self.delete_category_from_budget_url = reverse('delete_category_from_budget', args=[self.budget_category.id])
#         self.add_expense_to_budget_url = reverse('add_expense_to_budget', args=[self.budget.id])
#         self.update_budget_expense_url = reverse('update_budget_expense', args=[self.budget_expense.id])
#         self.delete_budget_expense_url = reverse('delete_budget_expense', args=[self.budget_expense.id])
#
#     def test_expense_view_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.expenses_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/expenses.html')
#         self.assertContains(response, 'expenses')
#
#         total_amount = Expense.objects.filter(author=self.user).aggregate(Sum('amount'))['amount__sum'] or 0
#         self.assertEqual(response.context['total_amount'], total_amount)
#
#     def test_expense_view_not_authenticated_user(self):
#         response = self.client.get(self.expenses_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_expense_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.create_expense_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/create_expense.html')
#         self.assertContains(response, 'form')
#
#     def test_create_expense_get_not_authenticated_user(self):
#         response = self.client.get(self.create_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_expense_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Create Test Expense',
#             'date': timezone.now().date(),
#             'amount': 5000,
#             'category': self.category.id
#         }
#         response = self.client.post(self.create_expense_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/expenses.html')
#
#         self.assertTrue(Expense.objects.filter(name='Create Test Expense').exists())
#
#         expense = Expense.objects.get(name='Create Test Expense')
#         self.assertEqual(expense.author, self.user)
#
#     def test_create_expense_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Create Test Expense',
#             'date': 10,
#             'amount': -5000,
#             'category': self.category.id
#         }
#         response = self.client.post(self.create_expense_url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/create_expense.html')
#
#         self.assertFalse(Expense.objects.filter(name='Create Test Expense').exists())
#
#     def test_create_expense_post_not_authenticated_user(self):
#         data = {
#             'name': 'Create Test Expense',
#             'date': timezone.now().date(),
#             'amount': 5000,
#             'category': self.category.id
#         }
#         response = self.client.post(self.create_expense_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_budget_expense_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.add_expense_to_budget_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/add_budget_expense.html')
#         self.assertContains(response, 'form')
#
#     def test_create_budget_expense_get_not_authenticated_user(self):
#         response = self.client.get(self.add_expense_to_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_budget_expense_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Create Test Budget Expense',
#             'date': timezone.now().date(),
#             'amount': 5000,
#             'category': self.budget_category.id
#         }
#
#         response = self.client.post(self.add_expense_to_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/details_budget.html')
#
#         self.assertTrue(BudgetExpense.objects.filter(name='Create Test Budget Expense').exists())
#
#         expense = BudgetExpense.objects.get(name='Create Test Budget Expense')
#         self.assertEqual(expense.author, self.user)
#
#     def test_create_budget_expense_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Create Test Budget Expense',
#             'date': 55,
#             'amount': -5000,
#             'category': self.budget_category.id
#         }
#
#         response = self.client.post(self.add_expense_to_budget_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/add_budget_expense.html')
#
#         self.assertFalse(Expense.objects.filter(name='Create Test Budget Expense').exists())
#
#     def test_create_budget_expense_post_not_authenticated_user(self):
#         data = {
#             'name': 'Create Test Budget Expense',
#             'date': timezone.now().date(),
#             'amount': 5000,
#             'category': self.budget_category.id
#         }
#
#         response = self.client.post(self.add_expense_to_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_budget_expense_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.update_budget_expense_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/update_expense.html')
#         self.assertContains(response, 'form')
#
#     def test_update_budget_expense_get_not_authenticated_user(self):
#         response = self.client.get(self.update_budget_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_budget_expense_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Updated Budget Expense',
#             'date': timezone.now().date(),
#             'amount': 50.05,
#             'category': self.budget_category.id,
#         }
#
#         response = self.client.post(self.update_budget_expense_url, data)
#
#         self.budget_expense.refresh_from_db()
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/details_budget.html')
#         self.assertEqual(self.budget_expense.name, 'Updated Budget Expense')
#         self.assertEqual(self.budget_expense.amount, Decimal('50.05'))
#
#     def test_update_budget_expense_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Updated Budget Expense',
#             'date': 55,
#             'amount': -50.05,
#             'category': self.budget_category.id,
#         }
#
#         response = self.client.post(self.update_budget_expense_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/update_expense.html')
#
#         self.assertFalse(Expense.objects.filter(name='Updated Budget Expense').exists())
#
#     def test_delete_budget_expense_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.delete_budget_expense_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/delete_expense.html')
#
#     def test_delete_budget_expense_get_not_authenticated_user(self):
#         response = self.client.get(self.delete_budget_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_budget_expense_post_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.post(self.delete_budget_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/details_budget.html')
#
#         self.assertFalse(BudgetExpense.objects.filter(name='Test Budget Expense').exists())
#
#     def test_delete_budget_expense_post_not_authenticated_user(self):
#         response = self.client.post(self.delete_budget_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_expense_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.update_expense_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/update_expense.html')
#         self.assertContains(response, 'form')
#
#     def test_update_expense_get_not_authenticated_user(self):
#         response = self.client.get(self.update_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_expense_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Updated Test Expense',
#             'date': timezone.now().date(),
#             'amount': 50.50,
#             'category': self.category.id,
#         }
#
#         response = self.client.post(self.update_expense_url, data)
#
#         self.assertEqual(response.status_code, 302)
#
#         self.expense.refresh_from_db()
#         self.assertEqual(self.expense.name, 'Updated Test Expense')
#         self.assertEqual(self.expense.amount, Decimal('50.50'))
#         self.assertTemplateUsed('expenses/expenses.html')
#
#     def test_update_expense_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Invalid Test Expense',
#             'date': 55,
#             'amount': -50.50,
#             'category': self.category.id,
#         }
#
#         response = self.client.post(self.update_expense_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.expense.refresh_from_db()
#         self.assertNotEqual(self.expense.name, 'Invalid Test Expense')
#         self.assertTemplateUsed('expenses/update_expense.html')
#
#     def test_update_expense_post_not_authenticated_user(self):
#         data = {
#             'name': 'Updated Test Expense',
#             'date': timezone.now().date(),
#             'amount': 50.50,
#             'category': self.category.id,
#         }
#
#         response = self.client.post(self.update_expense_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_expense_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.delete_expense_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/delete_expense.html')
#
#     def test_delete_expense_get_not_authenticated_user(self):
#         response = self.client.get(self.delete_expense_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_expense_post_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.post(self.delete_expense_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/expenses.html')
#
#     def test_delete_expense_post_not_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.post(self.delete_expense_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_category_list_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.list_categories_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/list_categories.html')
#         self.assertIn('categories', response.context)
#
#     def test_category_list_not_authenticated_user(self):
#         response = self.client.get(self.list_categories_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_category_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.create_category_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/create_category.html')
#         self.assertContains(response, 'form')
#
#     def test_create_category_get_not_authenticated_user(self):
#         response = self.client.get(self.create_category_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_category_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Create Test Category',
#         }
#
#         response = self.client.post(self.create_category_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/list_categories.html')
#
#         self.assertTrue(Category.objects.filter(name='Create Test Category').exists())
#
#     def test_create_category_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': '',
#         }
#
#         response = self.client.post(self.create_category_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/create_category.html')
#
#         self.assertFalse(Category.objects.filter(name='').exists())
#
#     def test_create_category_post_not_authenticated_user(self):
#         data = {
#             'name': 'Create Test Category',
#         }
#
#         response = self.client.post(self.create_category_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_category_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.update_category_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/update_category.html')
#         self.assertContains(response, 'form')
#
#     def test_update_category_get_not_authenticated_user(self):
#         response = self.client.get(self.update_category_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_category_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Updated Test Category',
#         }
#
#         response = self.client.post(self.update_category_url, data)
#
#         self.assertEqual(response.status_code, 302)
#
#         self.category.refresh_from_db()
#         self.assertEqual(self.category.name, 'Updated Test Category')
#         self.assertTemplateUsed('expenses/list_categories.html')
#
#     def test_update_category_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': '',
#         }
#
#         response = self.client.post(self.update_category_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.category.refresh_from_db()
#         self.assertNotEqual(self.category.name, '')
#         self.assertTemplateUsed(response, 'expenses/update_category.html')
#
#     def test_update_category_post_not_authenticated_user(self):
#         data = {
#             'name': 'Updated Test Category',
#         }
#
#         response = self.client.post(self.update_category_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_category_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.delete_category_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/delete_category.html')
#
#     def test_delete_category_get_not_authenticated_user(self):
#         response = self.client.get(self.delete_category_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_category_post_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.post(self.delete_category_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/list_categories.html')
#
#         self.assertFalse(Category.objects.filter(name='Test Category').exists())
#
#     def test_delete_category_post_not_authenticated_user(self):
#         response = self.client.post(self.delete_category_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_budget_list_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.budgets_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/budgets.html')
#         self.assertContains(response, 'budgets')
#
#     def test_budget_list_not_authenticated_user(self):
#         response = self.client.get(self.budgets_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_budget_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.create_budget_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/create_budget.html')
#         self.assertContains(response, 'form')
#
#     def test_create_budget_get_not_authenticated_user(self):
#         response = self.client.get(self.create_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_create_budget_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Create Test Budget',
#             'amount_to_spend': 2000,
#             'start_date': timezone.now().date(),
#             'end_date': timezone.now().date(),
#         }
#
#         response = self.client.post(self.create_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/details_budget.html')
#
#         self.assertTrue(Budget.objects.filter(name='Create Test Budget').exists())
#
#     def test_create_budget_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': '',
#             'amount_to_spend': -2000,
#             'start_date': timezone.now().date(),
#             'end_date': timezone.now().date(),
#         }
#
#         response = self.client.post(self.create_budget_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/create_budget.html')
#
#         self.assertFalse(Budget.objects.filter(name='').exists())
#
#     def test_create_budget_post_not_authenticated_user(self):
#         data = {
#             'name': 'Create Test Budget',
#             'amount_to_spend': 2000,
#             'start_date': timezone.now().date(),
#             'end_date': timezone.now().date(),
#         }
#
#         response = self.client.post(self.create_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_budget_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.update_budget_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/update_budget.html')
#         self.assertContains(response, 'form')
#
#     def test_update_budget_get_not_authenticated_user(self):
#         response = self.client.get(self.update_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_update_budget_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': 'Updated Test Budget',
#             'amount_to_spend': 3000,
#             'start_date': timezone.now().date(),
#             'end_date': timezone.now().date(),
#         }
#
#         response = self.client.post(self.update_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#
#         self.budget.refresh_from_db()
#         self.assertEqual(self.budget.name, 'Updated Test Budget')
#         self.assertTemplateUsed('expenses/details_budget.html')
#
#     def test_update_budget_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'name': '',
#             'amount_to_spend': -3000,
#             'start_date': timezone.now().date(),
#             'end_date': timezone.now().date(),
#         }
#
#         response = self.client.post(self.update_budget_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.budget.refresh_from_db()
#         self.assertNotEqual(self.budget.name, '')
#         self.assertTemplateUsed(response, 'expenses/update_budget.html')
#
#     def test_update_budget_post_not_authenticated_user(self):
#         data = {
#             'name': 'Updated Test Budget',
#             'amount_to_spend': 3000,
#             'start_date': timezone.now().date(),
#             'end_date': timezone.now().date(),
#         }
#
#         response = self.client.post(self.update_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_budget_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.delete_budget_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/delete_budget.html')
#
#     def test_delete_budget_get_not_authenticated_user(self):
#         response = self.client.get(self.delete_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_budget_post_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.post(self.delete_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/budgets.html')
#
#         self.assertFalse(Budget.objects.filter(name='Test Budget').exists())
#
#     def test_delete_budget_post_not_authenticated_user(self):
#         response = self.client.post(self.delete_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_details_budget_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.budget_details_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/details_budget.html')
#         self.assertContains(response, 'budget')
#
#     def test_details_budget_not_authenticated_user(self):
#         response = self.client.get(self.budget_details_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_add_category_to_budget_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.add_category_to_budget_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'budget')
#         self.assertContains(response, 'form')
#         self.assertTemplateUsed('expenses/add_budget_category.html')
#
#     def test_add_category_to_budget_get_not_authenticated_user(self):
#         response = self.client.get(self.add_category_to_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_add_category_to_budget_post_authenticated_user_valid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'category': self.category_budget.id,
#             'value': 100.05
#         }
#
#         response = self.client.post(self.add_category_to_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/details_budget.html')
#         self.assertTrue(BudgetCategory.objects.filter(budget=self.budget, category=self.category_budget, value=100.05).exists())
#
#     def test_add_category_to_budget_post_authenticated_user_invalid_data(self):
#         self.client.login(username='testuser', password='testpassword')
#         data = {
#             'category': self.category.id,
#             'value': -100.05
#         }
#
#         response = self.client.post(self.add_category_to_budget_url, data)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'expenses/add_budget_category.html')
#         self.assertIn('form', response.context)
#         self.assertFalse(BudgetCategory.objects.filter(budget=self.budget, value='100.05').exists())
#
#     def test_add_category_to_budget_post_not_authenticated_user(self):
#         data = {
#             'category': self.category_budget.id,
#             'value': 100.05
#         }
#
#         response = self.client.post(self.add_category_to_budget_url, data)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_category_from_budget_get_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.get(self.delete_category_from_budget_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed('expenses/delete_budget_category.html')
#
#     def test_delete_category_from_budget_get_not_authenticated_user(self):
#         response = self.client.get(self.delete_category_from_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
#
#     def test_delete_category_from_budget_post_authenticated_user(self):
#         self.client.login(username='testuser', password='testpassword')
#
#         response = self.client.post(self.delete_category_from_budget_url)
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('expenses/details_budget.html')
#         self.assertFalse(BudgetCategory.objects.filter(budget=self.budget, category=self.category, value=100.10).exists())
#
#     def test_delete_category_from_budget_post_not_authenticated_user(self):
#         response = self.client.post(self.delete_category_from_budget_url)
#
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('registration/login.html')
