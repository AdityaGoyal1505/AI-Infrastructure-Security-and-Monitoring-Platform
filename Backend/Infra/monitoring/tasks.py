from celery import shared_task  # type: ignore
from .services import process_event
from .models import Workspace,RootCauseAnalysis
from .ai.root_cause_engine import generate_root_cause
from .ai.recommendation_engine import store_recommendations
from .ai.trend_engine import generate_rca_trends,generate_node_trends,generate_correlation_trends
from .ai.trend_analyzer import analyze_alert_trends
from .ai.prediction_engine import generate_risk_prediction


@shared_task
def process_event_task(event_data):

    process_event(event_data)


@shared_task
def generate_root_cause_task(workspace_id, node_id):

    workspace = Workspace.objects.get(id=workspace_id)

    rca = generate_root_cause(workspace,node_id)

    if rca:

        generate_recommendations_task.delay(rca.id)

    generate_trend_insights_task.delay()

    generate_trend_snapshot_task.delay()

    generate_prediction_task.delay()


@shared_task
def generate_recommendations_task(rca_id):

    rca = RootCauseAnalysis.objects.get(id=rca_id)

    store_recommendations(rca.workspace,rca.node_id,rca)


@shared_task
def generate_trend_snapshot_task():

    analyze_alert_trends()


@shared_task
def generate_trend_insights_task():

    generate_rca_trends()

    generate_node_trends()

    generate_correlation_trends()
    print("[TREND INSIGHTS GENERATED]")


@shared_task
def generate_prediction_task():

    generate_risk_prediction()