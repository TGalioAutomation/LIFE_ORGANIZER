from django.contrib import admin
from .models import GoalCategory, Goal, GoalProgress, GoalMilestone, JournalEntry, MonthlyReview

@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'is_default', 'created_at']
    list_filter = ['is_default', 'user']
    search_fields = ['name', 'user__username']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'goal_type', 'status', 'progress_percentage', 'target_date']
    list_filter = ['goal_type', 'status', 'frequency', 'target_date']
    search_fields = ['title', 'user__username']
    date_hierarchy = 'target_date'

@admin.register(GoalProgress)
class GoalProgressAdmin(admin.ModelAdmin):
    list_display = ['goal', 'progress_date', 'value', 'completed']
    list_filter = ['progress_date', 'completed']
    search_fields = ['goal__title']

@admin.register(GoalMilestone)
class GoalMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'target_date', 'is_completed']
    list_filter = ['target_date', 'is_completed']
    search_fields = ['title', 'goal__title']

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'entry_date', 'title', 'mood_rating', 'is_private']
    list_filter = ['entry_date', 'mood_rating', 'is_private']
    search_fields = ['user__username', 'title', 'content']
    date_hierarchy = 'entry_date'

@admin.register(MonthlyReview)
class MonthlyReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review_month', 'overall_satisfaction', 'created_at']
    list_filter = ['review_month', 'overall_satisfaction']
    search_fields = ['user__username']
