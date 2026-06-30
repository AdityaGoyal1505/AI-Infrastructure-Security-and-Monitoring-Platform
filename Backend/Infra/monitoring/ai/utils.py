from django.utils import timezone
from datetime import timedelta
from monitoring.models import HealthScore

def get_health_bucket(score):

    if score is None:
        return -1

    return int(score // 5)

def get_latest_health_score(workspace_id, node_id=None, within_minutes=None):
    """Return the most recent HealthScore for a given workspace (and optional node).
    Args:
        workspace_id (int): Workspace identifier.
        node_id (str|int, optional): Node identifier. If omitted, returns the latest
            score across all nodes in the workspace.
        within_minutes (int, optional): Restricts to scores updated within the last
            *within_minutes* minutes.
    Returns:
        HealthScore | None: Latest HealthScore instance or ``None`` if none exist.
    """
    qs = HealthScore.objects.filter(workspace_id=workspace_id)
    if node_id is not None:
        qs = qs.filter(node_id=node_id)
    if within_minutes is not None:
        cutoff = timezone.now() - timedelta(minutes=within_minutes)
        qs = qs.filter(updated_at__gte=cutoff)
    return qs.order_by('-updated_at').first()