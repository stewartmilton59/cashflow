from django.contrib import admin
from apps.sales.models import Sale 

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('amount', 'payment_method', 'timestamp')
    list_filter = ('payment_method', 'timestamp')
    search_fields = ('amount',)
    ordering = ('-timestamp',)