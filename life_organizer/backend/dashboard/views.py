from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

from .models import DashboardWidget, Notification, UserActivity, DashboardPreference
from .serializers import (
    DashboardWidgetSerializer, NotificationSerializer, UserActivitySerializer,
    DashboardPreferenceSerializer, DashboardOverviewSerializer, QuickStatsSerializer,
    ActivityFeedSerializer, WidgetDataSerializer, DashboardAnalyticsSerializer,
    NotificationSummarySerializer, UserEngagementSerializer
)

# Import models from other apps
from expenses.models import Transaction, Budget
from tasks.models import Task
from goals.models import Goal, GoalProgress

# Import models from other apps for dashboard data
from expenses.models import Transaction, Budget
from tasks.models import Task
from goals.models import Goal, GoalProgress


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing dashboard widgets"""
    serializer_class = DashboardWidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DashboardWidget.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def reset_layout(self, request):
        """Reset dashboard layout to default"""
        # Delete existing widgets
        self.get_queryset().delete()

        # Create default widgets
        default_widgets = [
            {
                'widget_type': 'expense_summary',
                'title': 'Expense Summary',
                'position_x': 0, 'position_y': 0,
                'width': 2, 'height': 1
            },
            {
                'widget_type': 'task_summary',
                'title': 'Task Summary',
                'position_x': 2, 'position_y': 0,
                'width': 2, 'height': 1
            },
            {
                'widget_type': 'goal_progress',
                'title': 'Goal Progress',
                'position_x': 0, 'position_y': 1,
                'width': 2, 'height': 1
            },
            {
                'widget_type': 'recent_transactions',
                'title': 'Recent Transactions',
                'position_x': 2, 'position_y': 1,
                'width': 2, 'height': 2
            },
        ]

        created_widgets = []
        for widget_data in default_widgets:
            widget = DashboardWidget.objects.create(
                user=request.user,
                **widget_data
            )
            created_widgets.append(widget)

        serializer = self.get_serializer(created_widgets, many=True)
        return Response({
            'message': 'Dashboard layout reset to default',
            'widgets': serializer.data
        })

    @action(detail=False, methods=['get'])
    def widget_data(self, request):
        """Get data for all widgets"""
        widgets = self.get_queryset().filter(is_visible=True)
        widget_data = []

        for widget in widgets:
            data = self._get_widget_data(widget, request.user)
            widget_data.append({
                'widget_id': widget.id,
                'widget_type': widget.widget_type,
                'title': widget.title,
                'data': data,
                'last_updated': timezone.now()
            })

        return Response(widget_data)

    def _get_widget_data(self, widget, user):
        """Get data for a specific widget type"""
        if widget.widget_type == 'expense_summary':
            return self._get_expense_summary_data(user)
        elif widget.widget_type == 'task_summary':
            return self._get_task_summary_data(user)
        elif widget.widget_type == 'goal_progress':
            return self._get_goal_progress_data(user)
        elif widget.widget_type == 'recent_transactions':
            return self._get_recent_transactions_data(user)
        else:
            return {}

    def _get_expense_summary_data(self, user):
        """Get expense summary data"""
        now = timezone.now()
        current_month = now.replace(day=1).date()

        transactions = Transaction.objects.filter(
            user=user,
            transaction_date__date__gte=current_month
        )

        income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0

        expenses = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        return {
            'income': float(income),
            'expenses': float(expenses),
            'net': float(income - expenses),
            'period': 'This Month'
        }

    def _get_task_summary_data(self, user):
        """Get task summary data"""
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assignee=user)
        ).distinct()

        return {
            'total': tasks.count(),
            'completed': tasks.filter(status='done').count(),
            'pending': tasks.filter(status__in=['todo', 'in_progress']).count(),
            'overdue': tasks.filter(
                due_date__lt=timezone.now(),
                status__in=['todo', 'in_progress']
            ).count()
        }

    def _get_goal_progress_data(self, user):
        """Get goal progress data"""
        goals = Goal.objects.filter(user=user, status='active')

        if not goals.exists():
            return {'goals': [], 'average_progress': 0}

        goal_data = []
        total_progress = 0

        for goal in goals[:5]:  # Limit to 5 goals
            goal_data.append({
                'id': goal.id,
                'title': goal.title,
                'progress': goal.progress_percentage,
                'target_date': goal.target_date
            })
            total_progress += goal.progress_percentage

        return {
            'goals': goal_data,
            'average_progress': total_progress / len(goal_data)
        }

    def _get_recent_transactions_data(self, user):
        """Get recent transactions data"""
        transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')[:10]

        transaction_data = []
        for transaction in transactions:
            transaction_data.append({
                'id': transaction.id,
                'description': transaction.description,
                'amount': float(transaction.amount),
                'type': transaction.transaction_type,
                'date': transaction.transaction_date,
                'category': transaction.expense_category.name if transaction.expense_category else
                           transaction.income_category.name if transaction.income_category else 'Uncategorized'
            })

        return {'transactions': transaction_data}


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['notification_type', 'priority', 'is_read']
    ordering = ['-created_at']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'message': 'Notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({'message': 'All notifications marked as read'})

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get notification summary"""
        queryset = self.get_queryset()

        total = queryset.count()
        unread = queryset.filter(is_read=False).count()
        high_priority = queryset.filter(priority='high', is_read=False).count()
        recent = queryset.order_by('-created_at')[:5]

        summary_data = {
            'total_notifications': total,
            'unread_notifications': unread,
            'high_priority_count': high_priority,
            'recent_notifications': self.get_serializer(recent, many=True).data
        }

        return Response(summary_data)


class UserActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user activities"""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['activity_type']
    ordering = ['-created_at']

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)

        activities = self.get_queryset().filter(
            created_at__gte=start_date
        ).order_by('-created_at')[:20]

        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics"""
        queryset = self.get_queryset()

        # Activity by type
        activity_types = dict(
            queryset.values('activity_type').annotate(
                count=Count('activity_type')
            ).values_list('activity_type', 'count')
        )

        # Daily activity (last 7 days)
        daily_activity = []
        for i in range(7):
            day = timezone.now().date() - timedelta(days=i)
            count = queryset.filter(created_at__date=day).count()
            daily_activity.append({
                'date': day,
                'count': count
            })

        daily_activity.reverse()

        return Response({
            'activity_by_type': activity_types,
            'daily_activity': daily_activity,
            'total_activities': queryset.count()
        })


class DashboardOverviewView(APIView):
    """Dashboard overview with key metrics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            now = timezone.now()
            current_month = now.replace(day=1).date()

            # Financial summary
            transactions = Transaction.objects.filter(
                user=user,
                transaction_date__date__gte=current_month
            )

            total_income = transactions.filter(transaction_type='income').aggregate(
                total=Sum('amount')
            )['total'] or 0

            total_expenses = transactions.filter(transaction_type='expense').aggregate(
                total=Sum('amount')
            )['total'] or 0

            net_amount = total_income - total_expenses

            # Budget usage
            budgets = Budget.objects.filter(user=user, month=current_month)
            total_budget = budgets.aggregate(total=Sum('amount'))['total'] or 0
            budget_used_percentage = (total_expenses / total_budget * 100) if total_budget > 0 else 0

            # Task summary
            tasks = Task.objects.filter(
                Q(created_by=user) | Q(assignee=user)
            ).distinct()

            total_tasks = tasks.count()
            completed_tasks = tasks.filter(status='done').count()
            pending_tasks = tasks.filter(status__in=['todo', 'in_progress']).count()
            overdue_tasks = tasks.filter(
                due_date__lt=now,
                status__in=['todo', 'in_progress']
            ).count()

            # Goal summary
            goals = Goal.objects.filter(user=user)
            total_goals = goals.count()
            active_goals = goals.filter(status='active').count()
            completed_goals = goals.filter(status='completed').count()

            # Average goal progress - Fix the field name issue
            active_goals_with_progress = goals.filter(status='active')
            if active_goals_with_progress.exists():
                # Calculate progress percentage from current_value and target_value
                total_progress = 0
                count = 0
                for goal in active_goals_with_progress:
                    if goal.target_value and goal.target_value > 0:
                        progress = (goal.current_value / goal.target_value) * 100
                        total_progress += min(progress, 100)  # Cap at 100%
                        count += 1
                average_goal_progress = total_progress / count if count > 0 else 0
            else:
                average_goal_progress = 0

            # Recent data
            recent_transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')[:5]
            upcoming_tasks = Task.objects.filter(
                Q(created_by=user) | Q(assignee=user),
                due_date__gte=now,
                status__in=['todo', 'in_progress']
            ).distinct().order_by('due_date')[:5]

            goal_milestones = Goal.objects.filter(
                user=user,
                status='active'
            ).order_by('target_date')[:5]

            overview_data = {
                'total_income': float(total_income),
                'total_expenses': float(total_expenses),
                'net_amount': float(net_amount),
                'budget_used_percentage': float(budget_used_percentage),
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'overdue_tasks': overdue_tasks,
                'total_goals': total_goals,
                'active_goals': active_goals,
                'completed_goals': completed_goals,
                'average_goal_progress': float(average_goal_progress),
                'recent_transactions': [
                    {
                        'id': t.id,
                        'description': t.description,
                        'amount': float(t.amount),
                        'type': t.transaction_type,
                        'date': t.transaction_date
                    } for t in recent_transactions
                ],
                'upcoming_tasks': [
                    {
                        'id': t.id,
                        'title': t.title,
                        'due_date': t.due_date,
                        'priority': t.priority
                    } for t in upcoming_tasks
                ],
                'goal_milestones': [
                    {
                        'id': g.id,
                        'title': g.title,
                        'progress': (g.current_value / g.target_value * 100) if g.target_value > 0 else 0,
                        'target_date': g.target_date
                    } for g in goal_milestones
                ]
            }

            return Response(overview_data)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch dashboard overview', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardPreferencesView(APIView):
    """Dashboard preferences management"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get user's dashboard preferences"""
        try:
            preferences = DashboardPreference.objects.get(user=request.user)
            serializer = DashboardPreferenceSerializer(preferences)
            return Response(serializer.data)
        except DashboardPreference.DoesNotExist:
            # Create default preferences
            preferences = DashboardPreference.objects.create(user=request.user)
            serializer = DashboardPreferenceSerializer(preferences)
            return Response(serializer.data)

    def patch(self, request):
        """Update dashboard preferences"""
        try:
            preferences = DashboardPreference.objects.get(user=request.user)
        except DashboardPreference.DoesNotExist:
            preferences = DashboardPreference.objects.create(user=request.user)

        serializer = DashboardPreferenceSerializer(
            preferences,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuickStatsView(APIView):
    """Quick statistics for dashboard"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        period = request.query_params.get('period', 'month')

        # Calculate date range based on period
        now = timezone.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now.replace(day=1)
        elif period == 'year':
            start_date = now.replace(month=1, day=1)
        else:
            start_date = now - timedelta(days=30)

        # Financial stats
        transactions = Transaction.objects.filter(
            user=user,
            transaction_date__gte=start_date
        )

        income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0

        expenses = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Top expense categories
        top_categories = transactions.filter(
            transaction_type='expense'
        ).values(
            'expense_category__name'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')[:5]

        # Task stats
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assignee=user),
            created_at__gte=start_date
        ).distinct()

        completed_tasks = tasks.filter(status='done').count()
        total_tasks = tasks.count()
        task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Goal stats
        goals = Goal.objects.filter(user=user, created_at__gte=start_date)
        completed_goals = goals.filter(status='completed').count()
        total_goals = goals.count()
        goal_completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0

        # Habit streaks
        habit_goals = Goal.objects.filter(user=user, goal_type='habit', status='active')
        habit_streaks = []
        for habit in habit_goals:
            # Calculate current streak (simplified)
            recent_progress = GoalProgress.objects.filter(
                goal=habit,
                progress_date__gte=now.date() - timedelta(days=7),
                completed=True
            ).count()
            habit_streaks.append(recent_progress)

        habit_streak_average = sum(habit_streaks) / len(habit_streaks) if habit_streaks else 0

        # Upcoming deadlines
        upcoming_deadlines = []

        # Task deadlines
        upcoming_tasks = Task.objects.filter(
            Q(created_by=user) | Q(assignee=user),
            due_date__gte=now,
            due_date__lte=now + timedelta(days=7),
            status__in=['todo', 'in_progress']
        ).distinct()[:5]

        for task in upcoming_tasks:
            upcoming_deadlines.append({
                'type': 'task',
                'title': task.title,
                'deadline': task.due_date,
                'priority': task.priority
            })

        # Goal deadlines
        upcoming_goals = Goal.objects.filter(
            user=user,
            target_date__gte=now.date(),
            target_date__lte=now.date() + timedelta(days=7),
            status='active'
        )[:5]

        for goal in upcoming_goals:
            upcoming_deadlines.append({
                'type': 'goal',
                'title': goal.title,
                'deadline': goal.target_date,
                'progress': goal.progress_percentage
            })

        stats_data = {
            'period': period,
            'income_vs_expenses': {
                'income': float(income),
                'expenses': float(expenses),
                'difference': float(income - expenses)
            },
            'top_expense_categories': [
                {
                    'category': cat['expense_category__name'],
                    'amount': float(cat['total'])
                } for cat in top_categories
            ],
            'budget_alerts': [],  # Could be populated from budget alerts
            'task_completion_rate': float(task_completion_rate),
            'average_task_completion_time': 0.0,  # Could be calculated
            'most_productive_day': 'Monday',  # Could be calculated
            'goal_completion_rate': float(goal_completion_rate),
            'habit_streak_average': float(habit_streak_average),
            'upcoming_deadlines': upcoming_deadlines
        }

        return Response(stats_data)
