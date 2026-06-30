from monitoring.models import HealthScore, RiskPrediction
from .analytics import get_node_analytics
from .openai_client import ask_openai
import json

def generate_risk_prediction():
    latest_scores = HealthScore.objects.all()

    for score in latest_scores:
        risk_score = 100 - score.score
        
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Get deterministic analytics
        analytics = get_node_analytics(score.workspace_id, score.node_id)

        # Build prompt for AI explanation using analytics (always generated, no Insufficient Data placeholder)
        prompt = (
            f"Generate a short, professional executive summary explaining the risk for node '{score.node_id}'. "
            f"Current Risk Level: {risk_level}, Score: {risk_score}. "
            f"Health Trend: {analytics['health_trend']}, "
            f"Stability Index: {analytics['stability_index']}, "
            f"Recent Anomalies: {analytics['anomaly_frequency']}, "
            f"Recent Alerts: {analytics['alert_frequency']}. "
            f"Estimated Failure Window: {analytics['estimated_failure_window']}. "
            "Explain WHY the AI predicted this risk, the main contributing metrics, expected impact, and confidence reasoning in a concise paragraph (2-3 sentences)."
        )
        # Use standard OpenAI call without JSON mode to get natural language explanation
        explanation = ask_openai(prompt)

        RiskPrediction.objects.update_or_create(
            workspace=score.workspace,
            node_id=score.node_id,
            defaults={
                "risk_score": risk_score,
                "risk_level": risk_level,
                "explanation": explanation
            }
        )