import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model for the application."""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('viewer', 'Viewer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Workspace(models.Model):
    """Represents a monitoring workspace for a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    api_key = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class NodeStatus(models.Model):
    """Tracks the status and resource usage of a monitored node."""
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('warning', 'Warning'),
    ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='nodes')
    node_id = models.CharField(max_length=100)
    source_service = models.CharField(max_length=100, default='telemetry-agent')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    cpu_usage = models.FloatField(default=0)
    memory_usage = models.FloatField(default=0)
    disk_usage = models.FloatField(default=0)
    network_usage = models.FloatField(default=0)
    process_count = models.IntegerField(default=0)
    agent_version = models.CharField(max_length=50, default='1.0.0')
    last_heartbeat = models.DateTimeField()
    last_seen = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('workspace', 'node_id')
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['node_id']),
            models.Index(fields=['status']),
            models.Index(fields=['last_heartbeat']),
        ]

    def __str__(self):
        return f"{self.node_id} - {self.status}"


class Event(models.Model):
    """Represents a telemetry or incident event."""
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

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='events')
    node_id = models.CharField(max_length=100, default='local-node')
    source_service = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='log')
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='INFO')
    message = models.TextField()
    raw_log = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    anomaly_score = models.FloatField(default=0)
    is_resolved = models.BooleanField(default=False)
    occurrence_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_hash = models.CharField(max_length=64, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['workspace', 'created_at']),
            models.Index(fields=['severity']),
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['source_service']),
        ]

    def __str__(self):
        return f"{self.source_service} - {self.severity}"


class Rule(models.Model):
    """Defines an evaluation rule for alerts or monitoring."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    metric = models.CharField(max_length=100)
    operator = models.CharField(max_length=10)
    threshold = models.FloatField()
    severity = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class RuleMatch(models.Model):
    """Records when a rule condition is met."""
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    observed_value = models.FloatField()
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rule.name} | {self.node_id} | {self.observed_value}"


class Anomaly(models.Model):
    """Represents a detected anomaly in metrics."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    metric_name = models.CharField(max_length=100)
    observed_value = models.FloatField()
    baseline_value = models.FloatField()
    anomaly_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metric_name} | {self.node_id} | {self.anomaly_score}"


class Alert(models.Model):
    """Represents an alert triggered in the system."""
    STATUS_CHOICES = [
        ("OPEN", "OPEN"),
        ("ACKNOWLEDGED", "ACKNOWLEDGED"),
        ("RESOLVED", "RESOLVED")
    ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.title} [{self.status}]"


class HealthScore(models.Model):
    """Tracks the health score of a monitored node."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    score = models.FloatField()
    status = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "node_id"],
                name="unique_workspace_node_health"
            )
        ]

    def __str__(self):
        return f"{self.node_id} [{self.score}]"

class HealthScoreHistory(models.Model):
    """
    Historical health score snapshots used for AI prediction,
    trend analysis, forecasting, and analytics.
    """
    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name="health_history")
    node_id = models.CharField(max_length=255, db_index=True)
    score = models.FloatField()
    status = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["workspace", "node_id", "-created_at"]),]

    def __str__(self):
        return (
            f"{self.node_id} | "
            f"{self.score} | "
            f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

class Correlation(models.Model):
    """Represents a correlation between different events or metrics."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    correlation_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class RootCauseAnalysis(models.Model):
    """Stores AI-generated root cause analysis."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    root_cause = models.TextField()
    summary = models.TextField()
    confidence = models.FloatField()
    recommendations = models.JSONField(default=list)
    raw_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.node_id} | {self.confidence}"


class Recommendation(models.Model):
    """Stores actionable recommendations based on root cause analysis."""
    PRIORITY_CHOICES = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
        ("CRITICAL", "CRITICAL")
    ]
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    root_cause_analysis = models.ForeignKey(RootCauseAnalysis, on_delete=models.CASCADE, related_name="recommendations_generated")
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    is_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.priority} | {self.title}"


class RCAInsight(models.Model):
    """Stores insights extracted from root cause analyses."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    insight_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    occurrence_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TrendSnapshot(models.Model):
    """Tracks historical trends in monitoring metrics."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100)
    current_value = models.FloatField()
    previous_value = models.FloatField()
    change_percentage = models.FloatField()
    trend_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class RiskPrediction(models.Model):
    """Stores AI-based risk predictions for a node."""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    node_id = models.CharField(max_length=255)
    risk_score = models.FloatField()
    risk_level = models.CharField(max_length=50)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "node_id"],
                name="unique_prediction_per_node"
            )
        ]