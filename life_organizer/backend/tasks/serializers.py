from rest_framework import serializers
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from .models import Project, Task, TaskComment, TaskAttachment, TaskReminder, TaskTimeLog


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    owner = UserSerializer(read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'workspace', 'owner', 'color',
            'is_archived', 'start_date', 'end_date', 'task_count',
            'completed_tasks', 'progress_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_task_count(self, obj):
        return obj.tasks.count()
    
    def get_completed_tasks(self, obj):
        return obj.tasks.filter(status='done').count()
    
    def get_progress_percentage(self, obj):
        total_tasks = obj.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = obj.tasks.filter(status='done').count()
        return (completed_tasks / total_tasks) * 100
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    assignee = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    workspace_name = serializers.CharField(source='workspace.name', read_only=True)
    subtask_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_overdue = serializers.ReadOnlyField()
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_name',
            'workspace', 'workspace_name', 'assignee', 'created_by',
            'priority', 'status', 'due_date', 'start_date', 'completed_at',
            'parent_task', 'estimated_hours', 'actual_hours', 'tags',
            'subtask_count', 'comment_count', 'is_overdue', 'completion_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_subtask_count(self, obj):
        return obj.subtasks.count()
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        if not validated_data.get('assignee'):
            validated_data['assignee'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Auto-set completed_at when status changes to done
        if validated_data.get('status') == 'done' and instance.status != 'done':
            from django.utils import timezone
            validated_data['completed_at'] = timezone.now()
        elif validated_data.get('status') != 'done':
            validated_data['completed_at'] = None
        
        return super().update(instance, validated_data)


class TaskCommentSerializer(serializers.ModelSerializer):
    """Serializer for TaskComment model"""
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class TaskAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for TaskAttachment model"""
    uploaded_by = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskAttachment
        fields = [
            'id', 'task', 'uploaded_by', 'file', 'file_url', 'filename',
            'file_size', 'created_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'filename', 'file_size', 'created_at']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None
    
    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        file = validated_data.get('file')
        if file:
            validated_data['filename'] = file.name
            validated_data['file_size'] = file.size
        return super().create(validated_data)


class TaskReminderSerializer(serializers.ModelSerializer):
    """Serializer for TaskReminder model"""
    user = UserSerializer(read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    
    class Meta:
        model = TaskReminder
        fields = [
            'id', 'task', 'task_title', 'user', 'reminder_time',
            'reminder_type', 'message', 'is_sent', 'sent_at', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_sent', 'sent_at', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TaskTimeLogSerializer(serializers.ModelSerializer):
    """Serializer for TaskTimeLog model"""
    user = UserSerializer(read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    duration_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskTimeLog
        fields = [
            'id', 'task', 'task_title', 'user', 'start_time', 'end_time',
            'description', 'duration_minutes', 'duration_hours', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'duration_minutes', 'created_at']
    
    def get_duration_hours(self, obj):
        if obj.duration_minutes:
            return round(obj.duration_minutes / 60, 2)
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TaskSummarySerializer(serializers.Serializer):
    """Serializer for task summary data"""
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class KanbanColumnSerializer(serializers.Serializer):
    """Serializer for Kanban board columns"""
    status = serializers.CharField()
    title = serializers.CharField()
    tasks = TaskSerializer(many=True)
    task_count = serializers.IntegerField()


class TaskAnalyticsSerializer(serializers.Serializer):
    """Serializer for task analytics data"""
    productivity_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    average_completion_time = serializers.DecimalField(max_digits=8, decimal_places=2)
    most_productive_day = serializers.CharField()
    priority_distribution = serializers.DictField()
    status_distribution = serializers.DictField()
    monthly_completion_trend = serializers.ListField()
