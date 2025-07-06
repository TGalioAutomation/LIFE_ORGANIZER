from django.contrib import admin
from .models import Project, Task, TaskComment, TaskAttachment, TaskReminder, TaskTimeLog

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'workspace', 'owner', 'is_archived', 'created_at']
    list_filter = ['workspace', 'is_archived', 'created_at']
    search_fields = ['name', 'owner__username']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assignee', 'priority', 'status', 'due_date']
    list_filter = ['priority', 'status', 'project', 'due_date']
    search_fields = ['title', 'assignee__username', 'created_by__username']
    date_hierarchy = 'due_date'

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['task__title', 'author__username', 'content']

@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'task', 'uploaded_by', 'file_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['filename', 'task__title']

@admin.register(TaskReminder)
class TaskReminderAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'reminder_time', 'reminder_type', 'is_sent']
    list_filter = ['reminder_type', 'is_sent', 'reminder_time']

@admin.register(TaskTimeLog)
class TaskTimeLogAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'start_time', 'duration_minutes']
    list_filter = ['start_time', 'user']
