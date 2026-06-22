from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.sales import views

name = 'sales'

urlpatterns = [
    path('', views.sales, name='sales'),
    path('accountant_dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('director_dashboard/', views.director_dashboard, name='director_dashboard'),
    path('add_sale/', views.add_sale, name='add_sale'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
