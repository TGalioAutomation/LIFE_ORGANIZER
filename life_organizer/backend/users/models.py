from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Personal Information
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Preferences
    theme_preference = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )
    currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')

    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    weekly_recap_email = models.BooleanField(default=True)

    # Workspace Settings
    default_workspace = models.CharField(
        max_length=20,
        choices=[('personal', 'Personal'), ('work', 'Work'), ('team', 'Team')],
        default='personal'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Workspace(models.Model):
    """Workspace for organizing tasks and goals"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    members = models.ManyToManyField(User, related_name='workspaces', blank=True)

    workspace_type = models.CharField(
        max_length=20,
        choices=[
            ('personal', 'Personal'),
            ('work', 'Work'),
            ('team', 'Team'),
            ('family', 'Family')
        ],
        default='personal'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.workspace_type})"

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"
        ordering = ['-created_at']
