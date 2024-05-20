from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Expense
from .forms import ExpenseCreationForm, CategoryCreationForm
from django.urls import reverse_lazy


class ExpensesView(LoginRequiredMixin, ListView):
    model = Expense
    context_object_name = 'expenses'
    template_name = 'expenses/expenses.html'
    login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = context['expenses'].filter(author=self.request.user)
        return context


class CreateExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'expenses/create_expense.html'
    form_class = ExpenseCreationForm
    success_url = reverse_lazy('expenses')
    login_url = 'login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'expenses/create_category.html'
    form_class = CategoryCreationForm
    success_url = reverse_lazy('list_categories')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expenses/list_categories.html'
    login_url = 'login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = context['categories'].filter(author=self.request.user)
        return context
