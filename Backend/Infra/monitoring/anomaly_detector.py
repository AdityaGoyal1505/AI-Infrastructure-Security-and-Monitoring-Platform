from statistics import mean
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

        anomaly = Anomaly.objects.create(

            workspace=workspace,

            node_id=node_id,

            metric_name=metric_name,

            observed_value=value,

            baseline_value=baseline,

            anomaly_score=anomaly_score
        )
        
        create_anomaly_alert(workspace,anomaly)
        print(
            f"[ANOMALY] "
            f"{metric_name} "
            f"{value}"
        )


def analyze_metrics(workspace,node_id,metadata):

    for metric_name, value in metadata.items():

        if metric_name not in ANOMALY_METRICS:
            continue

        if isinstance(value,(int, float)):
            detect_anomaly(workspace,node_id,metric_name,value)