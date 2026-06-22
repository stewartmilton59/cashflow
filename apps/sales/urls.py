from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.sales import views

name = 'sales'

urlpatterns = [
    path('', views.sales, name='sales'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
