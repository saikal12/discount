from django.db import models
from django.conf import settings


class SystemLog(models.Model):
    """A model for recording logs
    like login, logout create, update, delete"""
    ACTION_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='systemlog')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
