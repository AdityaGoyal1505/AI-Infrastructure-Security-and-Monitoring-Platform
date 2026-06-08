from .tasks import generate_root_cause_task

from .models import Alert,Anomaly,Correlation

def correlate_node(workspace,node_id):

    alerts = Alert.objects.filter(

        workspace=workspace,

        node_id=node_id,

        status="OPEN"
    )

    alert_titles = set(alert.title.lower() for alert in alerts)

    resource_matches = 0

    if "high cpu" in alert_titles:
        resource_matches += 1

    if "critical cpu" in alert_titles:
        resource_matches += 1

    if "high memory" in alert_titles:
        resource_matches += 1

    if "critical memory" in alert_titles:
        resource_matches += 1

    if "too many processes" in alert_titles:
        resource_matches += 1

    if resource_matches >= 2:

        Correlation.objects.update_or_create(

            workspace=workspace,

            node_id=node_id,

            correlation_type="RESOURCE_PRESSURE",

            defaults={

                "title":"Resource Saturation",

                "severity":"CRITICAL",

                "metadata": {
                    "matched_alerts":list(alert_titles)
                },

                "is_active":True
            }
        )

    else:

        Correlation.objects.filter(

            workspace=workspace,

            node_id=node_id,

            correlation_type="RESOURCE_PRESSURE"

        ).update(is_active=False)

    if ("critical memory" in alert_titles and "disk full" in alert_titles):

        Correlation.objects.update_or_create(

            workspace=workspace,

            node_id=node_id,

            correlation_type="SYSTEM_DEGRADATION",

            defaults={

                "title":"System Degradation",

                "severity":"CRITICAL",

                "metadata": {
                    "matched_alerts":list(alert_titles)
                },

                "is_active":True
            }
        )

    else:

        Correlation.objects.filter(

            workspace=workspace,

            node_id=node_id,

            correlation_type="SYSTEM_DEGRADATION"

        ).update(is_active=False)


    anomaly_count = Anomaly.objects.filter(

        workspace=workspace,

        node_id=node_id

    ).count()

    if anomaly_count >= 3:

        Correlation.objects.update_or_create(

            workspace=workspace,

            node_id=node_id,

            correlation_type="ANOMALY_STORM",

            defaults={

                "title":"Anomaly Storm",

                "severity":"WARNING",

                "metadata": {
                    "anomaly_count":anomaly_count
                },

                "is_active":True
            }
        )

    else:

        Correlation.objects.filter(

            workspace=workspace,

            node_id=node_id,

            correlation_type="ANOMALY_STORM"

        ).update(is_active=False)

    generate_root_cause_task.delay(workspace.id,node_id)
        
    print(

        f"[CORRELATION] "

        f"{node_id} analyzed"
    )