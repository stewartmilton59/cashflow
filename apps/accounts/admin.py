from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'phone_number', 'email')
    search_fields = ('name', 'branch', 'phone_number', 'email')
