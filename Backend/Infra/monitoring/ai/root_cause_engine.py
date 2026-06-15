import json

from monitoring.models import (
    Alert,
    Correlation,
    HealthScore,
    Anomaly,
    RootCauseAnalysis
)
from .openai_client import ask_openai

from .prompt_builder import build_root_cause_prompt


def generate_root_cause(workspace,node_id):

    alerts = list(

        Alert.objects.filter(
            workspace=workspace,
            node_id=node_id
        )
        .order_by("-created_at")[:10]
        .values_list("title",flat=True)
    )

    correlations = list(

        Correlation.objects.filter(
            workspace=workspace,
            node_id=node_id
        )
        .order_by("-created_at")[:5]
        .values_list("correlation_type",flat=True)
    )

    anomalies = list(

        Anomaly.objects.filter(
            workspace=workspace,
            node_id=node_id
        )
        .order_by("-created_at")[:10]
        .values("metric_name","observed_value","baseline_value")
    )

    health = HealthScore.objects.filter(workspace=workspace,node_id=node_id).first()

    context = {

        "node_id":node_id,
        "health_score":health.score if health else 100,
        "alerts":alerts,
        "correlations":correlations,
        "anomalies":anomalies
    }

    prompt = build_root_cause_prompt(context)

    response = ask_openai(prompt)

    data = json.loads(response)

    rca = RootCauseAnalysis.objects.create(
        workspace=workspace,
        node_id=node_id,
        root_cause=data["root_cause"],
        summary=data["summary"],
        confidence=data["confidence"],
        recommendations=data["recommendations"],
        raw_response=data
    )

    return rca