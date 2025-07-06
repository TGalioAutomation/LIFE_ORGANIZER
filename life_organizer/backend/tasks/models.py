from django.db import models
from django.contrib.auth.models import User
from users.models import Workspace


class Project(models.Model):
    """Projects for organizing tasks"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='projects')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')

    # Project settings
    color = models.CharField(max_length=7, default='#007bff')
    is_archived = models.BooleanField(default=False)

    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']


class Task(models.Model):
    """Main task model"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    # Task properties
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')

    # Dates
    due_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    # Task hierarchy
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')

    # Estimates and tracking
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Metadata
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status not in ['done', 'cancelled']:
            from django.utils import timezone
            return timezone.now() > self.due_date
        return False

    @property
    def completion_percentage(self):
        """Calculate completion percentage based on subtasks"""
        subtasks = self.subtasks.all()
        if not subtasks.exists():
            return 100 if self.status == 'done' else 0

        completed_subtasks = subtasks.filter(status='done').count()
        total_subtasks = subtasks.count()
        return (completed_subtasks / total_subtasks) * 100

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']


class TaskComment(models.Model):
    """Comments on tasks"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_comments')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.task.title} by {self.author.username}"

    class Meta:
        verbose_name = "Task Comment"
        verbose_name_plural = "Task Comments"
        ordering = ['-created_at']


class TaskAttachment(models.Model):
    """File attachments for tasks"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_attachments')

    file = models.FileField(upload_to='task_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # Size in bytes

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - {self.task.title}"

    class Meta:
        verbose_name = "Task Attachment"
        verbose_name_plural = "Task Attachments"
        ordering = ['-created_at']


class TaskReminder(models.Model):
    """Reminders for tasks"""
    REMINDER_TYPES = [
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('both', 'Both'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_reminders')

    reminder_time = models.DateTimeField()
    reminder_type = models.CharField(max_length=10, choices=REMINDER_TYPES, default='both')
    message = models.TextField(blank=True)

    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.reminder_time}"

    class Meta:
        verbose_name = "Task Reminder"
        verbose_name_plural = "Task Reminders"
        ordering = ['reminder_time']


class TaskTimeLog(models.Model):
    """Time tracking for tasks"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_time_logs')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)

    # Calculated field
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Calculate duration when saving"""
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            self.duration_minutes = int(duration.total_seconds() / 60)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Time log for {self.task.title} - {self.duration_minutes or 'Ongoing'} minutes"

    class Meta:
        verbose_name = "Task Time Log"
        verbose_name_plural = "Task Time Logs"
        ordering = ['-start_time']
