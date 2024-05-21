# Generated by Django 5.0.6 on 2024-05-19 13:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]