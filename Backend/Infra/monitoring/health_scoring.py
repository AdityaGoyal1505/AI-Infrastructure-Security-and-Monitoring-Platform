from .models import Alert, HealthScore, HealthScoreHistory

def calculate_health_score(workspace, node_id, metadata):
    print("=" * 50)
    print("calculate_health_score()")
    print("Workspace:", workspace.id)
    print("Node:", node_id)
    print("=" * 50)

    from .tasks import generate_root_cause_task, generate_prediction_task

    score = 100
    penalties = []

    # -------------------------
    # Telemetry
    # -------------------------

    cpu = metadata.get("cpu_usage", 0)
    memory = metadata.get("memory_usage", 0)
    disk = metadata.get("disk_usage", 0)

    # CPU
    if cpu >= 95:
        score -= 30
        penalties.append("critical_cpu")
    elif cpu >= 80:
        score -= 20
        penalties.append("high_cpu")
    elif cpu >= 60:
        score -= 10
        penalties.append("moderate_cpu")

    # Memory
    if memory >= 95:
        score -= 30
        penalties.append("critical_memory")
    elif memory >= 80:
        score -= 20
        penalties.append("high_memory")
    elif memory >= 60:
        score -= 10
        penalties.append("moderate_memory")

    # Disk
    if disk >= 95:
        score -= 30
        penalties.append("critical_disk")
    elif disk >= 80:
        score -= 20
        penalties.append("high_disk")
    elif disk >= 60:
        score -= 10
        penalties.append("moderate_disk")

    # -------------------------
    # -------------------------
    # Active Alerts (CAPPED)
    # -------------------------

    alerts = Alert.objects.filter(
        workspace=workspace,
        node_id=node_id,
        status="OPEN"
    )

    critical_alerts = alerts.filter(severity="CRITICAL").count()
    warning_alerts = alerts.filter(severity="WARNING").count()
    info_alerts = alerts.exclude(
        severity__in=["CRITICAL", "WARNING"]
    ).count()

    alert_penalty = 0

    # Critical alerts (maximum 20 points)
    if critical_alerts:
        alert_penalty += min(critical_alerts * 5, 20)

    # Warning alerts (maximum 10 points)
    if warning_alerts:
        alert_penalty += min(warning_alerts * 0.5, 10)

    # Info alerts (maximum 5 points)
    if info_alerts:
        alert_penalty += min(info_alerts * 0.25, 5)

    score -= alert_penalty

    if critical_alerts:
        penalties.append(f"{critical_alerts}_critical_alerts")

    if warning_alerts:
        penalties.append(f"{warning_alerts}_warning_alerts")

    if info_alerts:
        penalties.append(f"{info_alerts}_info_alerts")
    # -------------------------
    # Clamp
    # -------------------------

    score = max(0, min(100, score))

    # -------------------------
    # Status
    # -------------------------

    if score >= 90:
        status = "HEALTHY"

    elif score >= 70:
        status = "WARNING"

    elif score >= 40:
        status = "DEGRADED"

    else:
        status = "CRITICAL"

    # -------------------------
    # Persist
    # -------------------------

    HealthScore.objects.update_or_create(
        workspace=workspace,
        node_id=node_id,
        defaults={
            "score": score,
            "status": status,
            "metadata": {
                "penalties": penalties,
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
                "critical_alerts": critical_alerts,
                "warning_alerts": warning_alerts,
                "info_alerts": info_alerts,
                "alert_penalty": round(alert_penalty, 2),
            },
        },
    )

    HealthScoreHistory.objects.create(
        workspace=workspace,
        node_id=node_id,
        score=score,
        status=status,
        metadata={
            **metadata,
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "info_alerts": info_alerts,
            "alert_penalty": round(alert_penalty, 2),
        },
    )

    # -------------------------
    # AI Tasks
    # -------------------------

    if score < 50:
        generate_root_cause_task.delay(workspace.id, node_id)

    generate_prediction_task.delay()

    return score