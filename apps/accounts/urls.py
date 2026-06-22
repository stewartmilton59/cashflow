from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.accounts, name='accounts'),
    path('', views.login, name='login'),
    # Add next_page so Django knows to send them back to login
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)