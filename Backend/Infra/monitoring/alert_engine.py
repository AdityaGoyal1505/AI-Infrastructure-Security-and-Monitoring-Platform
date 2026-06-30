from .models import Alert

def create_rule_alert(workspace,rule_match):
    existing = Alert.objects.filter(
        workspace=workspace,
        node_id=workspace.node_id,
        title=rule_match.rule.name,          # or alert title
        status="OPEN"
    ).first()

    if not existing:
        Alert.objects.create(
            workspace=workspace,
            node_id=workspace.node_id,
            title=rule_match.rule.name,
            severity=rule_match.rule.severity,
            status="OPEN",
            metadata={

                "value":rule_match.observed_value
            }
        )

def create_anomaly_alert(workspace,anomaly):

    Alert.objects.create(

        workspace=workspace,

        node_id=anomaly.node_id,

        title=f"Anomaly: {anomaly.metric_name}",

        severity="WARNING",

        source="ANOMALY",

        metadata={

            "baseline":anomaly.baseline_value,

            "observed":anomaly.observed_value,

            "score":anomaly.anomaly_score
        }
    )