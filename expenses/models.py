from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField(default=datetime.date.today)
    amount = models.FloatField(validators=[
            MinValueValidator(0.0001)
        ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name