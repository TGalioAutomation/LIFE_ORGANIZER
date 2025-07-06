from rest_framework import serializers
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from .models import DashboardWidget, Notification, UserActivity, DashboardPreference


class DashboardWidgetSerializer(serializers.ModelSerializer):
    """Serializer for DashboardWidget model"""
    
    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'widget_type', 'title', 'position_x', 'position_y',
            'width', 'height', 'settings', 'is_visible',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'priority', 'title', 'message',
            'action_url', 'action_data', 'is_read', 'is_sent',
            'scheduled_for', 'sent_at', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'is_sent', 'sent_at', 'read_at', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for UserActivity model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description', 'metadata',
            'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class DashboardPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for DashboardPreference model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DashboardPreference
        fields = [
            'id', 'user', 'layout_type', 'default_expense_period',
            'default_task_view', 'show_budget_alerts', 'show_task_reminders',
            'show_goal_reminders', 'quick_expense_categories', 'quick_task_templates',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DashboardOverviewSerializer(serializers.Serializer):
    """Serializer for dashboard overview data"""
    # Financial summary
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    budget_used_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    # Task summary
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    
    # Goal summary
    total_goals = serializers.IntegerField()
    active_goals = serializers.IntegerField()
    completed_goals = serializers.IntegerField()
    average_goal_progress = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    # Recent activity
    recent_transactions = serializers.ListField()
    upcoming_tasks = serializers.ListField()
    goal_milestones = serializers.ListField()


class QuickStatsSerializer(serializers.Serializer):
    """Serializer for quick statistics"""
    period = serializers.CharField()
    
    # Financial stats
    income_vs_expenses = serializers.DictField()
    top_expense_categories = serializers.ListField()
    budget_alerts = serializers.ListField()
    
    # Productivity stats
    task_completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_task_completion_time = serializers.DecimalField(max_digits=8, decimal_places=2)
    most_productive_day = serializers.CharField()
    
    # Goal stats
    goal_completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    habit_streak_average = serializers.DecimalField(max_digits=8, decimal_places=2)
    upcoming_deadlines = serializers.ListField()


class ActivityFeedSerializer(serializers.Serializer):
    """Serializer for activity feed"""
    activity_type = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField()
    icon = serializers.CharField()
    color = serializers.CharField()
    action_url = serializers.URLField(required=False)


class WidgetDataSerializer(serializers.Serializer):
    """Serializer for widget-specific data"""
    widget_type = serializers.CharField()
    data = serializers.DictField()
    last_updated = serializers.DateTimeField()


class DashboardAnalyticsSerializer(serializers.Serializer):
    """Serializer for dashboard analytics"""
    # Time-based analytics
    daily_activity = serializers.ListField()
    weekly_trends = serializers.ListField()
    monthly_summary = serializers.DictField()
    
    # Performance metrics
    productivity_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    financial_health_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    goal_achievement_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    # Insights
    top_achievements = serializers.ListField()
    areas_for_improvement = serializers.ListField()
    recommendations = serializers.ListField()


class NotificationSummarySerializer(serializers.Serializer):
    """Serializer for notification summary"""
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    high_priority_count = serializers.IntegerField()
    recent_notifications = NotificationSerializer(many=True)


class UserEngagementSerializer(serializers.Serializer):
    """Serializer for user engagement metrics"""
    login_streak = serializers.IntegerField()
    total_sessions = serializers.IntegerField()
    average_session_duration = serializers.DecimalField(max_digits=8, decimal_places=2)
    most_active_time = serializers.CharField()
    feature_usage = serializers.DictField()
    last_activity = serializers.DateTimeField()
