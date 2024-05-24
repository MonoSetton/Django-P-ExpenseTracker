from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator


class Budget(models.Model):
    name = models.CharField(max_length=200)
    amount_to_spend = models.DecimalField(max_digits=10, decimal_places=2,
                                          validators=[
                                              MinValueValidator(0.01)
                                          ])
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    budget = models.ForeignKey(Budget, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[
                                     MinValueValidator(0.01)
                                 ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



