import logging
import math
from statistics import mean
from datetime import datetime, timedelta
from django.utils import timezone
from .alert_engine import create_anomaly_alert
from .models import Anomaly


HISTORY_SIZE = 5

ANOMALY_THRESHOLD = 0.5

metric_history = {}


ANOMALY_METRICS = {
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "process_count"
}

def detect_anomaly(workspace,node_id,metric_name,value):
    
    print(f"ANALYZING: {metric_name}={value}")

    history = metric_history.get(f"{node_id}:{metric_name}",[])
    
    history.append(float(value))
    print(f"HISTORY: {history}")
    if len(history) > HISTORY_SIZE:
        history.pop(0)

    metric_history[f"{node_id}:{metric_name}"] = history

    if len(history) < 5:
        return

    baseline = mean(history[:-1])

    if baseline == 0:
        return

    deviation = abs(value - baseline) / baseline

    anomaly_score = min(deviation/5,1.0)

    if deviation >= ANOMALY_THRESHOLD:
        # Check for recent existing anomaly for same node and metric
        recent_anomaly = (
            Anomaly.objects.filter(
                workspace=workspace,
                node_id=node_id,
                metric_name=metric_name,
                created_at__gte=timezone.now() - timedelta(minutes=5),
            )
            .order_by('-created_at')
            .first()
        )
        if recent_anomaly:
            # Update existing anomaly
            recent_anomaly.observed_value = value
            recent_anomaly.baseline_value = baseline
            recent_anomaly.anomaly_score = anomaly_score
            recent_anomaly.save()
            anomaly = recent_anomaly
        else:
            # Create new anomaly
            anomaly = Anomaly.objects.create(
                workspace=workspace,
                node_id=node_id,
                metric_name=metric_name,
                observed_value=value,
                baseline_value=baseline,
                anomaly_score=anomaly_score,
            )
        create_anomaly_alert(workspace, anomaly)
        print(
            f"[ANOMALY] {metric_name} {value}"
        )


def analyze_metrics(workspace,node_id,metadata):

    for metric_name, value in metadata.items():

        if metric_name not in ANOMALY_METRICS:
            continue

        if isinstance(value,(int, float)):
            detect_anomaly(workspace,node_id,metric_name,value)