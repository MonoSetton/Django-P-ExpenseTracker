from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=200)
    amount_to_spend = models.DecimalField(max_digits=10, decimal_places=2,
                                          validators=[
                                              MinValueValidator(0.01)
                                          ])
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()
    categories = models.ManyToManyField(Category, through='BudgetCategory')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BudgetCategory(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.budget.name} - {self.category.name}"


class Expense(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[
                                     MinValueValidator(0.01)
                                 ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BudgetExpense(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[
                                     MinValueValidator(0.01)
                                 ])
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


