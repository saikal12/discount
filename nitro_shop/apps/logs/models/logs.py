from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='systemlog')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
