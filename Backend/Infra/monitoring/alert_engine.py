from .models import Alert

def create_rule_alert(workspace,rule_match):

    Alert.objects.create(

        workspace=workspace,

        node_id=rule_match.node_id,

        title=rule_match.rule.name,

        severity=rule_match.rule.severity,

        source="RULE",

        metadata={

            "value":
            rule_match.observed_value
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

            "baseline":
            anomaly.baseline_value,

            "observed":
            anomaly.observed_value,

            "score":
            anomaly.anomaly_score
        }
    )