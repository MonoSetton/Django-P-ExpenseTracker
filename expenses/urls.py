from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.ExpensesView.as_view(), name='expenses'),
    path('create_expense/', views.CreateExpenseView.as_view(), name='create_expense'),
    path('update_expense/<str:pk>', views.UpdateExpenseView.as_view(), name='update_expense'),
    path('delete_expense/<str:pk>', views.DeleteExpenseView.as_view(), name='delete_expense'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('update_category/<str:pk>', views.UpdateCategoryView.as_view(), name='update_category'),
    path('delete_category/<str:pk>', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('list_categories/', views.CategoryListView.as_view(), name='list_categories'),
    path('budgets/', views.BudgetView.as_view(), name='budgets'),
    path('budget_details/<str:pk>', views.DetailsBudgetView.as_view(), name='budget_details'),
    path('create_budgets/', views.CreateBudgetView.as_view(), name='create_budget'),
    path('update_budget/<str:pk>', views.UpdateBudgetView.as_view(), name='update_budget'),
    path('delete_budgets/<str:pk>', views.DeleteBudgetView.as_view(), name='delete_budget'),
    path('budget/<str:pk>/add_category/', views.AddCategoryToBudget.as_view(), name='add_category_to_budget'),
    path('budget/<str:pk>/add_expense', views.CreateBudgetExpenseView.as_view(), name='add_expense_to_budget'),
    ]
