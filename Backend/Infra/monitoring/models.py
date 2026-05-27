import uuid
from django.db import models #type: ignore
from django.contrib.auth.models import AbstractUser #type: ignore


class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('viewer', 'Viewer'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.username


class Workspace(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspaces'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    api_key = models.CharField(
        max_length=255,
        unique=True,
        editable=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.api_key:

            self.api_key = str(uuid.uuid4())

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name


class Event(models.Model):

    EVENT_TYPES = [
        ('log', 'Log'),
        ('metric', 'Metric'),
        ('incident', 'Incident'),
    ]

    SEVERITY_LEVELS = [
        ('INFO', 'INFO'),
        ('WARNING', 'WARNING'),
        ('ERROR', 'ERROR'),
        ('CRITICAL', 'CRITICAL'),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='events'
    )

    source_service = models.CharField(
        max_length=100
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='log'
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_LEVELS,
        default='INFO'
    )

    message = models.TextField()

    raw_log = models.TextField()

    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    anomaly_score = models.FloatField(
        default=0
    )

    is_resolved = models.BooleanField(
        default=False
    )

    occurrence_count = models.IntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-created_at']

        indexes = [

            models.Index(
                fields=['severity']
            ),

            models.Index(
                fields=['event_type']
            ),

            models.Index(
                fields=['created_at']
            ),

            models.Index(
                fields=['source_service']
            ),
        ]

    def __str__(self):

        return (
            f"{self.source_service} - "
            f"{self.severity}"
        )