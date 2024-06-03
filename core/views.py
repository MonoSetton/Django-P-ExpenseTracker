from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from expenses.models import Expense, Budget
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class HomeView(LoginRequiredMixin, ListView):
    model = Expense
    context_object_name = 'expenses'
    template_name = 'core/home.html'
    login_url = '/login/'

    def get_queryset(self):
        today = datetime.today()

        first_day_last_month = (today.replace(day=1) - relativedelta(months=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        return Expense.objects.filter(
            author=self.request.user,
            date__range=(first_day_last_month, last_day_last_month)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.today()
        first_day_last_month = (today.replace(day=1) - relativedelta(months=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        total_amount = Expense.objects.filter(
            author=self.request.user,
            date__range=(first_day_last_month, last_day_last_month)
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        context['total_amount'] = total_amount

        context['expenses'] = self.get_queryset()

        context['budgets'] = Budget.objects.filter(author=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['expenses'] = context['expenses'].filter(name__icontains=search_input)

        context['search_input'] = search_input
        return context
