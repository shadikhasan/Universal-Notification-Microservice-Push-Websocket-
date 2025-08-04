# notifications/models.py
import secrets
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_urlsafe(32)  # Generates a 43-character secure key
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Notification(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title


