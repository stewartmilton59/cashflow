from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'accountant', 'branch', 'payment_method', 'amount', 'timestamp', 'description']
    list_filter = ['branch', 'payment_method', 'timestamp']
    search_fields = ['accountant__username', 'description']
    date_hierarchy = 'timestamp'