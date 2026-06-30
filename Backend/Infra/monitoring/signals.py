from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HealthScore, HealthScoreHistory

@receiver(post_save, sender=HealthScore)
def create_health_score_history(sender, instance, created, **kwargs):
    """Create an immutable historical record each time a HealthScore is saved.
    The record captures the same fields as the current snapshot.
    """
    HealthScoreHistory.objects.create(
        workspace=instance.workspace,
        node_id=instance.node_id,
        score=instance.score,
        status=instance.status,
        metadata=instance.metadata,
    )
