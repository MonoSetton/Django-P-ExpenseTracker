from django.contrib import admin
from django.urls import path, include
from accounts.decorators import unauthenticated_user
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', unauthenticated_user(LoginView.as_view()), name='login'),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('expenses.urls')),

]
