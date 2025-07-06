from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

from .models import Project, Task, TaskComment, TaskAttachment, TaskReminder, TaskTimeLog
from .serializers import (
    ProjectSerializer, TaskSerializer, TaskCommentSerializer,
    TaskAttachmentSerializer, TaskReminderSerializer, TaskTimeLogSerializer,
    TaskSummarySerializer, KanbanColumnSerializer, TaskAnalyticsSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing projects"""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['workspace', 'is_archived']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(workspace__members=self.request.user)
        ).distinct()

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a project"""
        project = self.get_object()
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can archive projects'},
                status=status.HTTP_403_FORBIDDEN
            )

        project.is_archived = True
        project.save()
        return Response({'message': 'Project archived successfully'})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore an archived project"""
        project = self.get_object()
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can restore projects'},
                status=status.HTTP_403_FORBIDDEN
            )

        project.is_archived = False
        project.save()
        return Response({'message': 'Project restored successfully'})


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tasks"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'priority', 'project', 'assignee']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['due_date', 'priority', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assignee=self.request.user) |
            Q(workspace__members=self.request.user)
        ).distinct()

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get tasks assigned to current user"""
        tasks = self.get_queryset().filter(assignee=request.user)

        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)

        # Filter by due date
        due_filter = request.query_params.get('due')
        if due_filter == 'today':
            today = timezone.now().date()
            tasks = tasks.filter(due_date__date=today)
        elif due_filter == 'overdue':
            tasks = tasks.filter(
                due_date__lt=timezone.now(),
                status__in=['todo', 'in_progress']
            )
        elif due_filter == 'upcoming':
            next_week = timezone.now() + timedelta(days=7)
            tasks = tasks.filter(
                due_date__gte=timezone.now(),
                due_date__lte=next_week,
                status__in=['todo', 'in_progress']
            )

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get task summary statistics"""
        queryset = self.get_queryset()

        total_tasks = queryset.count()
        completed_tasks = queryset.filter(status='done').count()
        pending_tasks = queryset.filter(status__in=['todo', 'in_progress']).count()
        overdue_tasks = queryset.filter(
            due_date__lt=timezone.now(),
            status__in=['todo', 'in_progress']
        ).count()

        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        summary_data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': completion_rate
        }

        serializer = TaskSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def start_timer(self, request, pk=None):
        """Start time tracking for a task"""
        task = self.get_object()

        # Check if there's already an active timer
        active_timer = TaskTimeLog.objects.filter(
            task=task,
            user=request.user,
            end_time__isnull=True
        ).first()

        if active_timer:
            return Response(
                {'error': 'Timer already running for this task'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new time log
        time_log = TaskTimeLog.objects.create(
            task=task,
            user=request.user,
            start_time=timezone.now(),
            description=request.data.get('description', '')
        )

        serializer = TaskTimeLogSerializer(time_log, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def stop_timer(self, request, pk=None):
        """Stop time tracking for a task"""
        task = self.get_object()

        # Find active timer
        active_timer = TaskTimeLog.objects.filter(
            task=task,
            user=request.user,
            end_time__isnull=True
        ).first()

        if not active_timer:
            return Response(
                {'error': 'No active timer found for this task'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Stop timer
        active_timer.end_time = timezone.now()
        active_timer.save()

        serializer = TaskTimeLogSerializer(active_timer, context={'request': request})
        return Response(serializer.data)


class TaskCommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing task comments"""
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskComment.objects.filter(
            Q(task__created_by=self.request.user) |
            Q(task__assignee=self.request.user) |
            Q(author=self.request.user)
        ).distinct()


class TaskAttachmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing task attachments"""
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskAttachment.objects.filter(
            Q(task__created_by=self.request.user) |
            Q(task__assignee=self.request.user) |
            Q(uploaded_by=self.request.user)
        ).distinct()


class TaskReminderViewSet(viewsets.ModelViewSet):
    """ViewSet for managing task reminders"""
    serializer_class = TaskReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskReminder.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming reminders"""
        now = timezone.now()
        next_24_hours = now + timedelta(hours=24)

        reminders = self.get_queryset().filter(
            reminder_time__gte=now,
            reminder_time__lte=next_24_hours,
            is_sent=False
        ).order_by('reminder_time')

        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)


class TaskTimeLogViewSet(viewsets.ModelViewSet):
    """ViewSet for managing task time logs"""
    serializer_class = TaskTimeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskTimeLog.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        """Get daily time tracking summary"""
        date_str = request.query_params.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            target_date = timezone.now().date()

        time_logs = self.get_queryset().filter(
            start_time__date=target_date,
            end_time__isnull=False
        )

        total_minutes = sum(log.duration_minutes or 0 for log in time_logs)
        total_hours = round(total_minutes / 60, 2) if total_minutes > 0 else 0

        # Group by task
        task_summary = defaultdict(int)
        for log in time_logs:
            task_summary[log.task.title] += log.duration_minutes or 0

        return Response({
            'date': target_date,
            'total_hours': total_hours,
            'total_minutes': total_minutes,
            'log_count': time_logs.count(),
            'task_breakdown': dict(task_summary)
        })


class KanbanBoardView(APIView):
    """Kanban board view for tasks"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        project_id = request.query_params.get('project')

        # Get tasks queryset
        tasks_queryset = Task.objects.filter(
            Q(created_by=user) | Q(assignee=user) | Q(workspace__members=user)
        ).distinct()

        if project_id:
            tasks_queryset = tasks_queryset.filter(project_id=project_id)

        # Define status columns
        status_columns = [
            {'status': 'todo', 'title': 'To Do'},
            {'status': 'in_progress', 'title': 'In Progress'},
            {'status': 'review', 'title': 'Review'},
            {'status': 'done', 'title': 'Done'},
        ]

        # Build kanban data
        kanban_data = []
        for column in status_columns:
            column_tasks = tasks_queryset.filter(status=column['status']).order_by('-created_at')

            kanban_data.append({
                'status': column['status'],
                'title': column['title'],
                'tasks': TaskSerializer(column_tasks, many=True, context={'request': request}).data,
                'task_count': column_tasks.count()
            })

        return Response(kanban_data)


class TaskCalendarView(APIView):
    """Calendar view for tasks"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get month and year from query params
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {'error': 'Invalid month or year'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate month start and end dates
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = datetime(year, month + 1, 1) - timedelta(days=1)

        # Get tasks for the month
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assignee=user) | Q(workspace__members=user),
            due_date__gte=month_start,
            due_date__lte=month_end
        ).distinct().order_by('due_date')

        # Group tasks by date
        calendar_data = defaultdict(list)
        for task in tasks:
            date_key = task.due_date.strftime('%Y-%m-%d')
            calendar_data[date_key].append(
                TaskSerializer(task, context={'request': request}).data
            )

        return Response({
            'month': month,
            'year': year,
            'tasks': dict(calendar_data),
            'total_tasks': tasks.count()
        })


class TaskAnalyticsView(APIView):
    """Analytics for tasks"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            # Default to last 30 days
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Get tasks in date range
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assignee=user),
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).distinct()

        # Calculate analytics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='done').count()

        # Productivity score (completion rate)
        productivity_score = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Average completion time
        completed_with_time = tasks.filter(
            status='done',
            completed_at__isnull=False
        )

        avg_completion_time = 0
        if completed_with_time.exists():
            total_time = sum([
                (task.completed_at - task.created_at).total_seconds() / 3600
                for task in completed_with_time
            ])
            avg_completion_time = total_time / completed_with_time.count()

        # Priority distribution
        priority_dist = dict(tasks.values('priority').annotate(count=Count('priority')).values_list('priority', 'count'))

        # Status distribution
        status_dist = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))

        # Monthly completion trend (last 6 months)
        monthly_trend = []
        for i in range(6):
            month_start = (timezone.now().replace(day=1) - timedelta(days=32*i)).replace(day=1)
            month_end = (month_start.replace(month=month_start.month + 1) - timedelta(days=1)) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1) - timedelta(days=1)

            month_completed = Task.objects.filter(
                Q(created_by=user) | Q(assignee=user),
                status='done',
                completed_at__gte=month_start,
                completed_at__lte=month_end
            ).distinct().count()

            monthly_trend.append({
                'month': month_start.strftime('%b %Y'),
                'completed_tasks': month_completed
            })

        monthly_trend.reverse()

        analytics_data = {
            'productivity_score': round(productivity_score, 2),
            'average_completion_time': round(avg_completion_time, 2),
            'most_productive_day': 'Monday',  # Could be calculated from data
            'priority_distribution': priority_dist,
            'status_distribution': status_dist,
            'monthly_completion_trend': monthly_trend
        }

        return Response(analytics_data)
