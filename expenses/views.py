from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Expense, Budget, BudgetCategory, BudgetExpense
from .forms import ExpenseForm, CategoryForm, BudgetForm, BudgetCategoryForm, BudgetExpenseForm
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import get_object_or_404


class ExpensesView(LoginRequiredMixin, ListView):
    model = Expense
    context_object_name = 'expenses'
    template_name = 'expenses/expenses.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = Expense.objects.filter(author=self.request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_amount'] = total_amount
        context['expenses'] = context['expenses'].filter(author=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['expenses'] = context['expenses'].filter(name__icontains=search_input)

        context['search_input'] = search_input

        return context


class CreateExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'expenses/create_expense.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('expenses')
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreateBudgetExpenseView(LoginRequiredMixin, CreateView):
    model = BudgetExpense
    template_name = 'expenses/add_budget_expense.html'
    form_class = BudgetExpenseForm
    success_url = reverse_lazy('budgets')
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['budget'] = Budget.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('budget_details', kwargs={'pk': self.kwargs['pk']})


class UpdateBudgetExpenseView(LoginRequiredMixin, UpdateView):
    model = BudgetExpense
    form_class = BudgetExpenseForm
    template_name = 'expenses/update_expense.html'
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        budget_expense = self.get_object()
        kwargs['budget'] = budget_expense.category.budget
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('budget_details', kwargs={'pk': self.get_object().category.budget.pk})


class DeleteBudgetExpenseView(LoginRequiredMixin, DeleteView):
    model = BudgetExpense
    context_object_name = 'expense'
    template_name = 'expenses/delete_expense.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('budget_details', kwargs={'pk': self.get_object().category.budget.pk})


class UpdateExpenseView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/update_expense.html'
    success_url = reverse_lazy('expenses')
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    model = Expense
    context_object_name = 'expense'
    template_name = 'expenses/delete_expense.html'
    success_url = reverse_lazy('expenses')
    login_url = '/login/'


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expenses/list_categories.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = context['categories'].filter(author=self.request.user)

        return context


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'expenses/create_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('list_categories')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'expenses/update_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('list_categories')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'expenses/delete_category.html'
    success_url = reverse_lazy('list_categories')
    login_url = '/login/'


class BudgetView(LoginRequiredMixin, ListView):
    model = Budget
    context_object_name = 'budgets'
    template_name = 'expenses/budgets.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budgets'] = context['budgets'].filter(author=self.request.user)

        return context


class DetailsBudgetView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = 'expenses/details_budget.html'
    context_object_name = 'budget'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget = self.get_object()
        context['budget_expenses'] = BudgetExpense.objects.filter(category__budget=budget)

        category_totals = []
        budget_categories = BudgetCategory.objects.filter(budget=budget)
        for budget_category in budget_categories:
            total_amount = BudgetExpense.objects.filter(category=budget_category).aggregate(Sum('amount'))['amount__sum'] or 0
            category_totals.append({
                'category': budget_category.category.name,
                'total_amount': total_amount,
                'category_budget': budget_category.value
            })

        context['category_totals'] = category_totals
        return context


class CreateBudgetView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = 'expenses/create_budget.html'
    form_class = BudgetForm
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('budget_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateBudgetView(LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = 'expenses/update_budget.html'
    form_class = BudgetForm
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('budget_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteBudgetView(LoginRequiredMixin, DeleteView):
    model = Budget
    context_object_name = 'budget'
    template_name = 'expenses/delete_budget.html'
    success_url = reverse_lazy('budgets')
    login_url = '/login/'


class AddCategoryToBudget(LoginRequiredMixin, CreateView):
    model = BudgetCategory
    form_class = BudgetCategoryForm
    context_object_name = 'budget'
    template_name = 'expenses/add_budget_category.html'
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['budget'] = get_object_or_404(Budget, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        budget = get_object_or_404(Budget, pk=self.kwargs['pk'])
        form.instance.budget = budget
        return super().form_valid(form)

    def get_success_url(self):
        budget_id = self.object.budget.id
        return reverse_lazy('budget_details', kwargs={'pk': budget_id})


class DeleteCategoryFromBudget(LoginRequiredMixin, DeleteView):
    model = BudgetCategory
    context_object_name = 'budget_category'
    template_name = 'expenses/delete_budget_category.html'
    login_url = '/login/'

    def get_success_url(self):
        budget_id = self.object.budget.id
        return reverse_lazy('budget_details', kwargs={'pk': budget_id})
