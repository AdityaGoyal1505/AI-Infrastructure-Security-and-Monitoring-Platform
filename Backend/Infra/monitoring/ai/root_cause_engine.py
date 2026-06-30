import json

from monitoring.models import (
    Alert,
    Correlation,
    HealthScore,
    Anomaly,
    RootCauseAnalysis
)
from .openai_client import ask_openai
from .utils import get_health_bucket
from .prompt_builder import build_root_cause_prompt


def generate_root_cause(workspace,node_id):

    health = HealthScore.objects.filter(
        workspace=workspace,
        node_id=node_id
    ).order_by("-updated_at").first()

    health_score = health.score if health else 100

    current_bucket = get_health_bucket(health_score)

    latest_rca = (

        RootCauseAnalysis.objects.filter(
            workspace=workspace,
            node_id=node_id
        ).order_by("-created_at").first()

    )

    if latest_rca:

        previous_bucket = (

            latest_rca.raw_response.get("bucket")

            if latest_rca.raw_response

            else None

        )

        if previous_bucket == current_bucket:

            print(

                f"[RCA] "

                f"Skipping "

                f"{node_id} "

                f"(bucket unchanged)"

            )

            return latest_rca
        
    print(

                f"[RCA] "

                f"Implemented "

                f"{node_id} "

                f"(bucket changed)"

            )
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



    context = {

        "node_id":node_id,
        "health_score":health_score,
        "alerts":alerts,
        "correlations":correlations,
        "anomalies":anomalies
    }
    print("Health:", health_score)
    print("Alerts:", alerts)
    print("Correlations:", correlations)
    print("Anomalies:", anomalies)
    prompt = build_root_cause_prompt(context)

    response = ask_openai(prompt,json_mode=True)
    
    data = json.loads(response)

    data["bucket"]=current_bucket
    
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