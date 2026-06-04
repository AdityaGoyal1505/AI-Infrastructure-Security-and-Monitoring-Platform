import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


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

    api_key = models.UUIDField(
    unique=True,
    editable=False,
    default=uuid.uuid4
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


class NodeStatus(models.Model):

    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('warning', 'Warning'),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='nodes'
    )

    node_id = models.CharField(
        max_length=100
    )

    source_service = models.CharField(
        max_length=100,
        default='telemetry-agent'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='online'
    )

    cpu_usage = models.FloatField(
        default=0
    )

    memory_usage = models.FloatField(
        default=0
    )

    disk_usage = models.FloatField(
        default=0
    )

    network_usage = models.FloatField(
        default=0
    )

    process_count = models.IntegerField(
        default=0
    )

    agent_version = models.CharField(
        max_length=50,
        default='1.0.0'
    )

    last_heartbeat = models.DateTimeField()

    last_seen = models.DateTimeField(
        auto_now=True
    )

    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            'workspace',
            'node_id'
        )

        indexes = [

            models.Index(
                fields=['workspace']
            ),

            models.Index(
                fields=['node_id']
            ),

            models.Index(
                fields=['status']
            ),

            models.Index(
                fields=['last_heartbeat']
            ),
        ]

    def __str__(self):

        return (
            f"{self.node_id} "
            f"- {self.status}"
        )
    
class Event(models.Model):

    EVENT_TYPES = [
        ('log', 'Log'),
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

    node_id = models.CharField(
        max_length=100,
        default='local-node'
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

    event_hash = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    
    class Meta:

        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=[
                    'workspace',
                    'created_at'
                ]
            ),

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
            f"{self.source_service} "
            f"- {self.severity}"
        )

class Rule(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    metric = models.CharField(
        max_length=50
    )

    operator = models.CharField(
        max_length=10
    )

    # scope = models.CharField(
    #     max_length=50,
    #     choices=[
    #         ("system", "System"),
    #         ("api", "API"),
    #         ("service", "Service")
    #     ]
    # )
    threshold = models.FloatField()
    severity = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    
class RuleMatch(models.Model):

    rule = models.ForeignKey(
        Rule,
        on_delete=models.CASCADE
    )

    node_id = models.CharField(
        max_length=255
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    observed_value = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )