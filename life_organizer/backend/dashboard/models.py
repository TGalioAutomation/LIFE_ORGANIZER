from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DashboardWidget(models.Model):
    """Configurable dashboard widgets"""
    WIDGET_TYPES = [
        ('expense_summary', 'Expense Summary'),
        ('budget_overview', 'Budget Overview'),
        ('task_summary', 'Task Summary'),
        ('goal_progress', 'Goal Progress'),
        ('recent_transactions', 'Recent Transactions'),
        ('upcoming_tasks', 'Upcoming Tasks'),
        ('mood_tracker', 'Mood Tracker'),
        ('quick_stats', 'Quick Statistics'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPES)

    # Widget configuration
    title = models.CharField(max_length=100)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=1)
    height = models.IntegerField(default=1)

    # Widget settings (JSON field for flexibility)
    settings = models.JSONField(default=dict, blank=True)

    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        verbose_name = "Dashboard Widget"
        verbose_name_plural = "Dashboard Widgets"
        ordering = ['position_y', 'position_x']


class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPES = [
        ('budget_alert', 'Budget Alert'),
        ('task_reminder', 'Task Reminder'),
        ('goal_reminder', 'Goal Reminder'),
        ('system', 'System Notification'),
        ('achievement', 'Achievement'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')

    title = models.CharField(max_length=255)
    message = models.TextField()

    # Optional action data
    action_url = models.URLField(blank=True)
    action_data = models.JSONField(default=dict, blank=True)

    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    # Timestamps
    scheduled_for = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']


class UserActivity(models.Model):
    """Track user activity for analytics"""
    ACTIVITY_TYPES = [
        ('login', 'User Login'),
        ('expense_added', 'Expense Added'),
        ('income_added', 'Income Added'),
        ('task_created', 'Task Created'),
        ('task_completed', 'Task Completed'),
        ('goal_created', 'Goal Created'),
        ('goal_updated', 'Goal Updated'),
        ('journal_entry', 'Journal Entry'),
        ('budget_created', 'Budget Created'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)

    # Activity details
    description = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)

    # Context
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ['-created_at']


class DashboardPreference(models.Model):
    """User preferences for dashboard customization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preferences')

    # Layout preferences
    layout_type = models.CharField(
        max_length=20,
        choices=[('grid', 'Grid Layout'), ('list', 'List Layout')],
        default='grid'
    )

    # Default date ranges
    default_expense_period = models.CharField(
        max_length=20,
        choices=[
            ('week', 'This Week'),
            ('month', 'This Month'),
            ('quarter', 'This Quarter'),
            ('year', 'This Year'),
        ],
        default='month'
    )

    default_task_view = models.CharField(
        max_length=20,
        choices=[
            ('kanban', 'Kanban Board'),
            ('list', 'List View'),
            ('calendar', 'Calendar View'),
        ],
        default='kanban'
    )

    # Notification preferences
    show_budget_alerts = models.BooleanField(default=True)
    show_task_reminders = models.BooleanField(default=True)
    show_goal_reminders = models.BooleanField(default=True)

    # Quick actions
    quick_expense_categories = models.JSONField(default=list, blank=True)
    quick_task_templates = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Dashboard Preferences"

    class Meta:
        verbose_name = "Dashboard Preference"
        verbose_name_plural = "Dashboard Preferences"
