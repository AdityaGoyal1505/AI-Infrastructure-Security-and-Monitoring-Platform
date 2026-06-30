# ai_services/chatbot.py

from monitoring.models import (
    HealthScore,
    Alert,
    Anomaly,
    RootCauseAnalysis,
    Recommendation,
    RiskPrediction
)

from .gemini_client import ask_gemini


def ask_inframind(workspace_id,question):

    health = HealthScore.objects.filter(workspace_id=workspace_id).order_by("-updated_at").first()


    alerts = list(Alert.objects.filter(workspace_id=workspace_id,status="OPEN").values_list("title",flat=True)[:5])


    anomalies = list(Anomaly.objects.filter(workspace_id=workspace_id).values("metric_name","observed_value")[:5])


    rca = RootCauseAnalysis.objects.filter(workspace_id=workspace_id).order_by("-created_at").first()


    recommendations = list(Recommendation.objects.filter(workspace_id=workspace_id).values_list("title",flat=True)[:5])


    risk = RiskPrediction.objects.filter(workspace_id=workspace_id).order_by("-created_at").first()


    prompt = f"""

You are InfraMind AI.

You ONLY answer:

- Infrastructure Monitoring

- Alerts

- Health Scores

- Root Cause Analysis

- Recommendations

- Risk Prediction

- Trends

If user asks unrelated questions,

politely refuse.



Workspace Data


Health Score:

{health.score if health else "N/A"}


Health Status:

{health.status if health else "N/A"}


Open Alerts:

{alerts}


Recent Anomalies:

{anomalies}


Latest RCA:

{rca.summary if rca else "N/A"}


Recommendations:

{recommendations}


Risk:

{risk.risk_level if risk else "N/A"}



User Question:

{question}


Rules:

1 Keep answer under 120 words

2 Use bullet points

3 Be concise

"""
    for _ in range(2):
        try: 
            return ask_gemini(prompt)
        except Exception:
            return (
                "AI assistant is currently experiencing high demand. "
                "Please try again shortly."
            )
    