from django.contrib import admin
from .models import UserProfile, Workspace

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme_preference', 'currency', 'created_at']
    list_filter = ['theme_preference', 'currency', 'default_workspace']
    search_fields = ['user__username', 'user__email']

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'workspace_type', 'owner', 'is_active', 'created_at']
    list_filter = ['workspace_type', 'is_active']
    search_fields = ['name', 'owner__username']
