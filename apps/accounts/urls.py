from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.accounts import views

name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
