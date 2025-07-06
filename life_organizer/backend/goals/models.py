from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class GoalCategory(models.Model):
    """Categories for organizing goals"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#28a745')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goal_categories')

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Goal Category"
        verbose_name_plural = "Goal Categories"
        unique_together = ['name', 'user']
        ordering = ['name']


class Goal(models.Model):
    """Personal goals and objectives"""
    GOAL_TYPES = [
        ('numeric', 'Numeric Target'),
        ('boolean', 'Yes/No Achievement'),
        ('habit', 'Daily/Weekly Habit'),
        ('financial', 'Financial Target'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One Time'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(GoalCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='goals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')

    # Goal properties
    goal_type = models.CharField(max_length=15, choices=GOAL_TYPES, default='boolean')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES, default='one_time')

    # Numeric targets (for numeric and financial goals)
    target_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    unit = models.CharField(max_length=50, blank=True)  # e.g., "books", "dollars", "hours"

    # Dates
    start_date = models.DateField()
    target_date = models.DateField()
    completed_at = models.DateTimeField(blank=True, null=True)

    # Settings
    is_public = models.BooleanField(default=False)
    reminder_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.goal_type == 'boolean':
            return 100 if self.status == 'completed' else 0
        elif self.goal_type in ['numeric', 'financial'] and self.target_value:
            if self.target_value == 0:
                return 0
            progress = (self.current_value / self.target_value) * 100
            return min(progress, 100)  # Cap at 100%
        return 0

    @property
    def is_overdue(self):
        """Check if goal is overdue"""
        if self.status in ['completed', 'cancelled']:
            return False
        from django.utils import timezone
        return timezone.now().date() > self.target_date

    @property
    def days_remaining(self):
        """Calculate days remaining to target date"""
        from django.utils import timezone
        if self.status in ['completed', 'cancelled']:
            return 0
        delta = self.target_date - timezone.now().date()
        return max(delta.days, 0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"
        ordering = ['-created_at']


class GoalProgress(models.Model):
    """Track daily/weekly progress on goals"""
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goal_progress')

    # Progress data
    progress_date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)

    # For habit tracking
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.goal.title} - {self.progress_date}: {self.value}"

    class Meta:
        verbose_name = "Goal Progress"
        verbose_name_plural = "Goal Progress Entries"
        unique_together = ['goal', 'progress_date']
        ordering = ['-progress_date']


class GoalMilestone(models.Model):
    """Milestones for breaking down large goals"""
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    target_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    target_date = models.DateField()

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.goal.title} - {self.title}"

    class Meta:
        verbose_name = "Goal Milestone"
        verbose_name_plural = "Goal Milestones"
        ordering = ['target_date']


class JournalEntry(models.Model):
    """Daily journal entries and reflections"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')

    entry_date = models.DateField()
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    # Mood tracking
    mood_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True,
        help_text="Rate your mood from 1 (worst) to 10 (best)"
    )

    # Tags for categorization
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")

    # Privacy
    is_private = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Journal Entry - {self.entry_date}"

    class Meta:
        verbose_name = "Journal Entry"
        verbose_name_plural = "Journal Entries"
        unique_together = ['user', 'entry_date']
        ordering = ['-entry_date']


class MonthlyReview(models.Model):
    """Monthly goal reviews and reflections"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_reviews')

    review_month = models.DateField()  # First day of the month

    # Review content
    achievements = models.TextField(help_text="What did you achieve this month?")
    challenges = models.TextField(help_text="What challenges did you face?")
    lessons_learned = models.TextField(help_text="What did you learn?")
    next_month_focus = models.TextField(help_text="What will you focus on next month?")

    # Ratings
    overall_satisfaction = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rate your overall satisfaction (1-10)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Monthly Review - {self.review_month.strftime('%B %Y')}"

    class Meta:
        verbose_name = "Monthly Review"
        verbose_name_plural = "Monthly Reviews"
        unique_together = ['user', 'review_month']
        ordering = ['-review_month']
