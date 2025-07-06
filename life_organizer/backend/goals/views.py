from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
import random

from .models import GoalCategory, Goal, GoalProgress, GoalMilestone, JournalEntry, MonthlyReview
from .serializers import (
    GoalCategorySerializer, GoalSerializer, GoalProgressSerializer,
    GoalMilestoneSerializer, JournalEntrySerializer, MonthlyReviewSerializer,
    GoalSummarySerializer, GoalAnalyticsSerializer, HabitTrackingSerializer,
    MotivationalInsightSerializer
)


class GoalCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing goal categories"""
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_defaults(self, request):
        """Create default goal categories for the user"""
        default_categories = [
            {'name': 'Personal Development', 'icon': 'self_improvement', 'color': '#2196F3'},
            {'name': 'Health & Fitness', 'icon': 'fitness_center', 'color': '#4CAF50'},
            {'name': 'Career', 'icon': 'work', 'color': '#FF9800'},
            {'name': 'Financial', 'icon': 'attach_money', 'color': '#9C27B0'},
            {'name': 'Relationships', 'icon': 'favorite', 'color': '#E91E63'},
            {'name': 'Education', 'icon': 'school', 'color': '#3F51B5'},
            {'name': 'Travel', 'icon': 'flight', 'color': '#00BCD4'},
            {'name': 'Hobbies', 'icon': 'palette', 'color': '#FF5722'},
        ]

        created_categories = []
        for cat_data in default_categories:
            category, created = GoalCategory.objects.get_or_create(
                user=request.user,
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'is_default': True
                }
            )
            if created:
                created_categories.append(category)

        serializer = self.get_serializer(created_categories, many=True)
        return Response({
            'message': f'Created {len(created_categories)} default categories',
            'categories': serializer.data
        })


class GoalViewSet(viewsets.ModelViewSet):
    """ViewSet for managing goals"""
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'goal_type', 'category', 'frequency']
    search_fields = ['title', 'description']
    ordering_fields = ['target_date', 'created_at', 'progress_percentage']
    ordering = ['-created_at']

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active goals"""
        goals = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue goals"""
        goals = self.get_queryset().filter(
            status='active',
            target_date__lt=timezone.now().date()
        )
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get goal summary statistics"""
        queryset = self.get_queryset()

        total_goals = queryset.count()
        active_goals = queryset.filter(status='active').count()
        completed_goals = queryset.filter(status='completed').count()
        paused_goals = queryset.filter(status='paused').count()
        overdue_goals = queryset.filter(
            status='active',
            target_date__lt=timezone.now().date()
        ).count()

        completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0

        # Calculate average progress for active goals
        active_goal_progress = queryset.filter(status='active').values_list('progress_percentage', flat=True)
        average_progress = sum(active_goal_progress) / len(active_goal_progress) if active_goal_progress else 0

        summary_data = {
            'total_goals': total_goals,
            'active_goals': active_goals,
            'completed_goals': completed_goals,
            'paused_goals': paused_goals,
            'overdue_goals': overdue_goals,
            'completion_rate': completion_rate,
            'average_progress': average_progress
        }

        serializer = GoalSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update goal progress"""
        goal = self.get_object()
        value = request.data.get('value', 0)
        notes = request.data.get('notes', '')
        completed = request.data.get('completed', False)

        # Create progress entry
        progress = GoalProgress.objects.create(
            goal=goal,
            user=request.user,
            progress_date=timezone.now().date(),
            value=value,
            notes=notes,
            completed=completed
        )

        # Update goal's current value
        if goal.goal_type in ['numeric', 'financial']:
            goal.current_value = value
            goal.save()

        return Response({
            'message': 'Progress updated successfully',
            'progress': GoalProgressSerializer(progress).data,
            'goal': self.get_serializer(goal).data
        })


class GoalProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for managing goal progress"""
    serializer_class = GoalProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent progress entries"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)

        progress = self.get_queryset().filter(
            progress_date__gte=start_date
        ).order_by('-progress_date')

        serializer = self.get_serializer(progress, many=True)
        return Response(serializer.data)


class GoalMilestoneViewSet(viewsets.ModelViewSet):
    """ViewSet for managing goal milestones"""
    serializer_class = GoalMilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalMilestone.objects.filter(goal__user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark milestone as completed"""
        milestone = self.get_object()
        milestone.is_completed = True
        milestone.completed_at = timezone.now()
        milestone.save()

        serializer = self.get_serializer(milestone)
        return Response(serializer.data)


class JournalEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing journal entries"""
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['entry_date', 'mood_rating']
    search_fields = ['title', 'content', 'tags']
    ordering = ['-entry_date']

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def mood_trends(self, request):
        """Get mood trends over time"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)

        entries = self.get_queryset().filter(
            entry_date__gte=start_date,
            mood_rating__isnull=False
        ).order_by('entry_date')

        mood_data = []
        for entry in entries:
            mood_data.append({
                'date': entry.entry_date,
                'mood': entry.mood_rating,
                'title': entry.title
            })

        # Calculate average mood
        avg_mood = sum(entry.mood_rating for entry in entries) / len(entries) if entries else 0

        return Response({
            'mood_trends': mood_data,
            'average_mood': round(avg_mood, 1),
            'total_entries': len(mood_data)
        })


class MonthlyReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing monthly reviews"""
    serializer_class = MonthlyReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-review_month']

    def get_queryset(self):
        return MonthlyReview.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """Get review for current month"""
        current_month = timezone.now().replace(day=1).date()

        try:
            review = self.get_queryset().get(review_month=current_month)
            serializer = self.get_serializer(review)
            return Response(serializer.data)
        except MonthlyReview.DoesNotExist:
            return Response(
                {'message': 'No review found for current month'},
                status=status.HTTP_404_NOT_FOUND
            )


class GoalAnalyticsView(APIView):
    """Analytics for goals"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            # Default to last 6 months
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=180)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Get goals in date range
        goals = Goal.objects.filter(
            user=user,
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )

        # Goal completion trend (monthly)
        completion_trend = []
        for i in range(6):
            month_start = (timezone.now().replace(day=1) - timedelta(days=32*i)).replace(day=1)
            month_end = (month_start.replace(month=month_start.month + 1) - timedelta(days=1)) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1) - timedelta(days=1)

            completed_goals = Goal.objects.filter(
                user=user,
                status='completed',
                completed_at__gte=month_start,
                completed_at__lte=month_end
            ).count()

            completion_trend.append({
                'month': month_start.strftime('%b %Y'),
                'completed_goals': completed_goals
            })

        completion_trend.reverse()

        # Category distribution
        category_dist = dict(
            goals.values('category__name').annotate(
                count=Count('category')
            ).values_list('category__name', 'count')
        )

        # Goal type distribution
        type_dist = dict(
            goals.values('goal_type').annotate(
                count=Count('goal_type')
            ).values_list('goal_type', 'count')
        )

        # Average goal duration
        completed_goals = goals.filter(status='completed', completed_at__isnull=False)
        avg_duration = 0
        if completed_goals.exists():
            total_duration = sum([
                (goal.completed_at.date() - goal.start_date).days
                for goal in completed_goals
            ])
            avg_duration = total_duration / completed_goals.count()

        analytics_data = {
            'goal_completion_trend': completion_trend,
            'category_distribution': category_dist,
            'goal_type_distribution': type_dist,
            'average_goal_duration': round(avg_duration, 2),
            'most_productive_month': 'January',  # Could be calculated
            'success_rate_by_category': category_dist  # Simplified
        }

        return Response(analytics_data)


class NextStepSuggestionsView(APIView):
    """AI-powered next step suggestions for goals"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get active goals
        active_goals = Goal.objects.filter(user=user, status='active')

        suggestions = []

        for goal in active_goals:
            # Generate suggestions based on goal progress and type
            if goal.progress_percentage < 25:
                suggestions.append({
                    'message': f"Break down '{goal.title}' into smaller, actionable steps",
                    'insight_type': 'planning',
                    'goal_id': goal.id,
                    'action_suggestion': 'Create 3-5 milestones for this goal'
                })
            elif goal.progress_percentage < 50:
                suggestions.append({
                    'message': f"You're making progress on '{goal.title}'! Keep the momentum going",
                    'insight_type': 'motivation',
                    'goal_id': goal.id,
                    'action_suggestion': 'Schedule daily 15-minute work sessions'
                })
            elif goal.progress_percentage < 75:
                suggestions.append({
                    'message': f"'{goal.title}' is more than halfway done! Push through to the finish",
                    'insight_type': 'encouragement',
                    'goal_id': goal.id,
                    'action_suggestion': 'Set a completion deadline for extra motivation'
                })
            else:
                suggestions.append({
                    'message': f"'{goal.title}' is almost complete! You're so close to achieving it",
                    'insight_type': 'final_push',
                    'goal_id': goal.id,
                    'action_suggestion': 'Dedicate focused time this week to finish'
                })

        # Add general motivational insights
        if not suggestions:
            suggestions.append({
                'message': "Ready to achieve something amazing? Create your first goal!",
                'insight_type': 'getting_started',
                'action_suggestion': 'Start with a small, achievable goal'
            })

        # Add habit tracking suggestions
        habit_goals = active_goals.filter(goal_type='habit')
        for habit in habit_goals:
            # Get recent progress
            recent_progress = GoalProgress.objects.filter(
                goal=habit,
                progress_date__gte=timezone.now().date() - timedelta(days=7)
            ).count()

            if recent_progress < 5:  # Less than 5 days in the last week
                suggestions.append({
                    'message': f"Consistency is key for '{habit.title}'. Try to maintain your daily habit",
                    'insight_type': 'habit_reminder',
                    'goal_id': habit.id,
                    'action_suggestion': 'Set a daily reminder at the same time each day'
                })

        # Randomize and limit suggestions
        random.shuffle(suggestions)
        suggestions = suggestions[:5]  # Limit to 5 suggestions

        return Response({
            'suggestions': suggestions,
            'total_active_goals': active_goals.count(),
            'generated_at': timezone.now()
        })


class HabitTrackingView(APIView):
    """Habit tracking analytics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get habit-type goals
        habits = Goal.objects.filter(user=user, goal_type='habit', status='active')

        habit_data = []
        for habit in habits:
            # Calculate streaks and completion rate
            progress_entries = GoalProgress.objects.filter(
                goal=habit,
                completed=True
            ).order_by('progress_date')

            # Current streak
            current_streak = 0
            today = timezone.now().date()
            check_date = today

            while True:
                if GoalProgress.objects.filter(
                    goal=habit,
                    progress_date=check_date,
                    completed=True
                ).exists():
                    current_streak += 1
                    check_date -= timedelta(days=1)
                else:
                    break

            # Longest streak (simplified calculation)
            longest_streak = current_streak  # Could be more sophisticated

            # Completion rate (last 30 days)
            last_30_days = timezone.now().date() - timedelta(days=30)
            completed_days = GoalProgress.objects.filter(
                goal=habit,
                progress_date__gte=last_30_days,
                completed=True
            ).count()
            completion_rate = (completed_days / 30) * 100

            # Weekly progress (last 7 days)
            weekly_progress = []
            for i in range(7):
                day = today - timedelta(days=i)
                completed = GoalProgress.objects.filter(
                    goal=habit,
                    progress_date=day,
                    completed=True
                ).exists()
                weekly_progress.append({
                    'date': day,
                    'completed': completed
                })

            weekly_progress.reverse()

            habit_data.append({
                'habit_name': habit.title,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'completion_rate': round(completion_rate, 1),
                'weekly_progress': weekly_progress
            })

        return Response({
            'habits': habit_data,
            'total_habits': len(habit_data)
        })
