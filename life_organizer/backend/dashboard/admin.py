from django.contrib import admin
from .models import DashboardWidget, Notification, UserActivity, DashboardPreference

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'widget_type', 'is_visible', 'position_x', 'position_y']
    list_filter = ['widget_type', 'is_visible', 'user']
    search_fields = ['title', 'user__username']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['title', 'user__username', 'message']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'

@admin.register(DashboardPreference)
class DashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'layout_type', 'default_expense_period', 'default_task_view']
    list_filter = ['layout_type', 'default_expense_period', 'default_task_view']
    search_fields = ['user__username']
