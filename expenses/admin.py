from django.contrib import admin
from .models import Expense, Category, Budget, BudgetCategory

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(BudgetCategory)