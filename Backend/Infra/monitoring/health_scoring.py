from .models import Alert,HealthScore

def calculate_health_score(workspace,node_id,metadata):

    from .tasks import generate_root_cause_task

    score = 100

    penalties = []

    cpu = metadata.get("cpu_usage",0)

    if cpu >= 95:

        score -= 30

        penalties.append("critical_cpu")

    elif cpu >= 80:

        score -= 20

        penalties.append("high_cpu")

    memory = metadata.get("memory_usage",0)

    if memory >= 95:

        score -= 30

        penalties.append("critical_memory")

    elif memory >= 80:

        score -= 20

        penalties.append("high_memory")
    
    disk = metadata.get("disk_usage",0)

    if disk >= 95:

        score -= 30

        penalties.append("critical_disk")

    elif disk >= 80:

        score -= 20

        penalties.append("high_disk")

    alerts = Alert.objects.filter(

        workspace=workspace,

        node_id=node_id,

        status="OPEN"
    )
    
    for alert in alerts:
        if alert.severity == "CRITICAL":

            score -= 15
        elif alert.severity == "WARNING":

            score -= 10
        else:

            score -= 5
    
    score = max(score,0)

    if score >= 90:

        status = "HEALTHY"

    elif score >= 70:

        status = "WARNING"

    elif score >= 40:

        status = "DEGRADED"

    else:

        status = "CRITICAL"

        HealthScore.objects.update_or_create(

            workspace=workspace,

            node_id=node_id,

            defaults={

                "score": score,

                "status": status,

                "metadata": {

                    "penalties":penalties,

                    "cpu":cpu,

                    "memory":memory,

                    "disk":disk,

                    "open_alerts":alerts.count()
                }
            }
    )
        
    if score < 50:
        generate_root_cause_task.delay(workspace.id,node_id)
    
    return score