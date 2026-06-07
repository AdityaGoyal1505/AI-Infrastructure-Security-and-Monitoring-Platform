from .models import Correlation,Incident


def detect_incidents(workspace,node_id):

    correlations = Correlation.objects.filter(
        workspace=workspace,
        node_id=node_id,
        is_active=True
    )

    if not correlations.exists():

        Incident.objects.filter(
            workspace=workspace,
            node_id=node_id,
            status="OPEN"
        ).update(status="RESOLVED")
        return

    severity = "INFO"

    for correlation in correlations:

        if correlation.severity == "CRITICAL":

            severity = "CRITICAL"

            break

        elif correlation.severity == "WARNING":

            severity = "WARNING"

    correlation_titles = [correlation.title for correlation in correlations]

    Incident.objects.update_or_create(

        workspace=workspace,

        node_id=node_id,

        status="OPEN",

        defaults={

            "title":f"{node_id}: "+ ", ".join(correlation_titles),

            "severity":severity,

            "metadata": {
                "correlations":correlation_titles
            }
        }
    )