from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Expense
from .forms import ExpenseCreationForm, CategoryCreationForm, ExpenseUpdateForm
from django.urls import reverse_lazy


class ExpensesView(LoginRequiredMixin, ListView):
    model = Expense
    context_object_name = 'expenses'
    template_name = 'expenses/expenses.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = context['expenses'].filter(author=self.request.user)
        return context


class CreateExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'expenses/create_expense.html'
    form_class = ExpenseCreationForm
    success_url = reverse_lazy('expenses')
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateExpenseView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseUpdateForm
    template_name = 'expenses/update_expense.html'
    success_url = reverse_lazy('expenses')
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    model = Expense
    context_object_name = 'expense'
    template_name = 'expenses/delete_expense.html'
    success_url = reverse_lazy('expenses')
    login_url = '/login/'


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'expenses/create_category.html'
    form_class = CategoryCreationForm
    success_url = reverse_lazy('list_categories')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expenses/list_categories.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = context['categories'].filter(author=self.request.user)
        return context


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'expenses/update_category.html'
    success_url = reverse_lazy('list_categories')
    login_url = '/login/'


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'expenses/delete_category.html'
    success_url = reverse_lazy('list_categories')
    login_url = '/login/'