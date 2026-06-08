import json

from .openai_client import ask_openai

from .prompt_builder import build_root_cause_prompt

from monitoring.models import RootCauseAnalysis,Alert,Correlation,HealthScore


def generate_root_cause(workspace,node_id):

    alerts = list(

        Alert.objects.filter(
            workspace=workspace,
            node_id=node_id
        )
        .order_by("-created_at")[:10]
        .values_list("title",flat=True
)
    )

    correlations = list(

        Correlation.objects.filter(
            workspace=workspace,
            node_id=node_id
        )
        .order_by("-created_at")[:5]
        .values_list("correlation_type",flat=True)
    )

    health = HealthScore.objects.filter(

        workspace=workspace,

        node_id=node_id

    ).first()

    context = {

        "node_id": node_id,

        "health_score":health.score if health else 100,

        "alerts": alerts,

        "correlations": correlations
    }

    prompt = build_root_cause_prompt(context)

    response = ask_openai(prompt)

    data = json.loads(response)

    RootCauseAnalysis.objects.create(

        workspace=workspace,

        node_id=node_id,

        root_cause=data["root_cause"],

        summary=data["summary"],

        confidence=data["confidence"],

        recommendations=data["recommendations"],

        raw_response=data
    )

    return data