from django.contrib import admin
from .models import ExpenseCategory, IncomeCategory, Transaction, Budget, BudgetAlert

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'is_default', 'created_at']
    list_filter = ['is_default', 'user']
    search_fields = ['name', 'user__username']

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'is_default', 'created_at']
    list_filter = ['is_default', 'user']
    search_fields = ['name', 'user__username']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'transaction_type', 'amount', 'user', 'transaction_date']
    list_filter = ['transaction_type', 'transaction_date', 'voice_input']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'transaction_date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'amount', 'month', 'percentage_used']
    list_filter = ['month', 'user']
    search_fields = ['category__name', 'user__username']

@admin.register(BudgetAlert)
class BudgetAlertAdmin(admin.ModelAdmin):
    list_display = ['budget', 'alert_type', 'is_read', 'sent_at']
    list_filter = ['alert_type', 'is_read', 'sent_at']
