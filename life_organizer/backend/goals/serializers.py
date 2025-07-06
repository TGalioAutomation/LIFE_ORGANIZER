from rest_framework import serializers
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from .models import GoalCategory, Goal, GoalProgress, GoalMilestone, JournalEntry, MonthlyReview


class GoalCategorySerializer(serializers.ModelSerializer):
    """Serializer for GoalCategory model"""
    goal_count = serializers.SerializerMethodField()
    active_goals = serializers.SerializerMethodField()
    
    class Meta:
        model = GoalCategory
        fields = [
            'id', 'name', 'description', 'icon', 'color', 'is_default',
            'goal_count', 'active_goals', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_default', 'created_at', 'updated_at']
    
    def get_goal_count(self, obj):
        return obj.goals.count()
    
    def get_active_goals(self, obj):
        return obj.goals.filter(status='active').count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GoalMilestoneSerializer(serializers.ModelSerializer):
    """Serializer for GoalMilestone model"""
    
    class Meta:
        model = GoalMilestone
        fields = [
            'id', 'goal', 'title', 'description', 'target_value',
            'target_date', 'is_completed', 'completed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for Goal model"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    user = UserSerializer(read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    milestones = GoalMilestoneSerializer(many=True, read_only=True)
    milestone_count = serializers.SerializerMethodField()
    completed_milestones = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 'user',
            'goal_type', 'status', 'frequency', 'target_value', 'current_value',
            'unit', 'start_date', 'target_date', 'completed_at', 'is_public',
            'reminder_enabled', 'progress_percentage', 'is_overdue', 'days_remaining',
            'milestones', 'milestone_count', 'completed_milestones',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_milestone_count(self, obj):
        return obj.milestones.count()
    
    def get_completed_milestones(self, obj):
        return obj.milestones.filter(is_completed=True).count()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Auto-set completed_at when status changes to completed
        if validated_data.get('status') == 'completed' and instance.status != 'completed':
            from django.utils import timezone
            validated_data['completed_at'] = timezone.now()
        elif validated_data.get('status') != 'completed':
            validated_data['completed_at'] = None
        
        return super().update(instance, validated_data)


class GoalProgressSerializer(serializers.ModelSerializer):
    """Serializer for GoalProgress model"""
    goal_title = serializers.CharField(source='goal.title', read_only=True)
    
    class Meta:
        model = GoalProgress
        fields = [
            'id', 'goal', 'goal_title', 'progress_date', 'value',
            'notes', 'completed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        # Update goal's current_value if this is the latest progress
        goal = validated_data['goal']
        if goal.goal_type in ['numeric', 'financial']:
            goal.current_value = validated_data['value']
            goal.save()
        
        return super().create(validated_data)


class JournalEntrySerializer(serializers.ModelSerializer):
    """Serializer for JournalEntry model"""
    user = UserSerializer(read_only=True)
    word_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JournalEntry
        fields = [
            'id', 'user', 'entry_date', 'title', 'content', 'mood_rating',
            'tags', 'is_private', 'word_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_word_count(self, obj):
        return len(obj.content.split()) if obj.content else 0
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MonthlyReviewSerializer(serializers.ModelSerializer):
    """Serializer for MonthlyReview model"""
    user = UserSerializer(read_only=True)
    month_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MonthlyReview
        fields = [
            'id', 'user', 'review_month', 'month_name', 'achievements',
            'challenges', 'lessons_learned', 'next_month_focus',
            'overall_satisfaction', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_month_name(self, obj):
        return obj.review_month.strftime('%B %Y')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GoalSummarySerializer(serializers.Serializer):
    """Serializer for goal summary data"""
    total_goals = serializers.IntegerField()
    active_goals = serializers.IntegerField()
    completed_goals = serializers.IntegerField()
    paused_goals = serializers.IntegerField()
    overdue_goals = serializers.IntegerField()
    completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_progress = serializers.DecimalField(max_digits=5, decimal_places=2)


class GoalAnalyticsSerializer(serializers.Serializer):
    """Serializer for goal analytics data"""
    goal_completion_trend = serializers.ListField()
    category_distribution = serializers.DictField()
    goal_type_distribution = serializers.DictField()
    average_goal_duration = serializers.DecimalField(max_digits=8, decimal_places=2)
    most_productive_month = serializers.CharField()
    success_rate_by_category = serializers.DictField()


class HabitTrackingSerializer(serializers.Serializer):
    """Serializer for habit tracking data"""
    habit_name = serializers.CharField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    weekly_progress = serializers.ListField()


class MotivationalInsightSerializer(serializers.Serializer):
    """Serializer for motivational insights"""
    message = serializers.CharField()
    insight_type = serializers.CharField()
    goal_id = serializers.IntegerField(required=False)
    action_suggestion = serializers.CharField(required=False)
