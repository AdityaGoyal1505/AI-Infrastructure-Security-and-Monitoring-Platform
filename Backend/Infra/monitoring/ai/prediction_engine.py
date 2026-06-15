from monitoring.models import HealthScore, RiskPrediction

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

        explanation = (
            f"Node {score.node_id} "
            f"has health score {score.score}"
        )

        RiskPrediction.objects.update_or_create(

            workspace=score.workspace,

            node_id=score.node_id,

            defaults={

                "risk_score": risk_score,

                "risk_level": risk_level,

                "explanation": explanation
            }
        )