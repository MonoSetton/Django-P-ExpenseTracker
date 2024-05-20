from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.ExpensesView.as_view(), name='expenses'),
    path('create_expense/', views.CreateExpenseView.as_view(), name='create_expense'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('list_categories/', views.CategoryListView.as_view(), name='list_categories'),
    ]
