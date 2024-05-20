from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import Expense


class HomeView(LoginRequiredMixin, ListView):
    model = Expense
    context_object_name = 'expenses'
    template_name = 'core/home.html'
    login_url = 'login/'

