from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.decorators import unauthenticated_user
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', unauthenticated_user(LoginView.as_view()), name='login'),
    path('', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('expenses.urls')),
    path('', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
