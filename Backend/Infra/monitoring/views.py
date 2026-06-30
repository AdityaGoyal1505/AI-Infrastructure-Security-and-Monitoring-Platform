import os
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError  # type:ignore
from rest_framework_simplejwt.tokens import RefreshToken  # type:ignore

from .tasks import process_event_task
from .ai.chatbot import ask_inframind
from monitoring.models import (
    Workspace, Alert, Anomaly, HealthScore, HealthScoreHistory, TrendSnapshot,
    RCAInsight, Recommendation, RiskPrediction, RootCauseAnalysis
)
from .serializers import (
    RootCauseAnalysisSerializer,
    RecommendationSerializer,
    HealthScoreSerializer,
    AnomalySerializer,
    RCAInsightSerializer,
    RiskPredictionSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    WorkspaceSerializer,
    WorkspaceCreateSerializer,
    WorkspaceSetupSerializer
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """Handles user registration."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handles user login and sets JWT cookies."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {"user": UserSerializer(user).data},
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None"
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None"
        )
        return response


class LogoutView(APIView):
    """Handles user logout by deleting JWT cookies."""
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CookieTokenRefreshView(APIView):
    """Handles refreshing JWT tokens via cookies."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"message": "Token refreshed"})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60 * 60
            )
            return response
        except TokenError:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class CurrentUserView(APIView):
    """Returns the currently authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkspaceListCreateView(APIView):
    """Lists workspaces for a user or creates a new one."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workspaces = Workspace.objects.filter(user=request.user).order_by("-created_at")
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkspaceCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            workspace = serializer.save()
            return Response(WorkspaceSerializer(workspace).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceDetailView(APIView):
    """Retrieves, updates, or deletes a specific workspace."""
    permission_classes = [IsAuthenticated]

    def get_workspace(self, request, workspace_id):
        return get_object_or_404(Workspace, id=workspace_id, user=request.user)

    def get(self, request, workspace_id):
        workspace = self.get_workspace(request, workspace_id)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, workspace_id):
        workspace = self.get_workspace(request, workspace_id)
        serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workspace_id):
        workspace = self.get_workspace(request, workspace_id)
        workspace.delete()
        return Response({"message": "Workspace deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class WorkspaceSetupView(APIView):
    """Provides setup details for a workspace."""
    permission_classes = [IsAuthenticated]

    def get(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id, user=request.user)
        data = {
            "workspace_id": workspace.id,
            "workspace_name": workspace.name,
            "api_key": workspace.api_key,
            "download_url": f"/api/workspaces/{workspace.id}/agent/"
        }
        serializer = WorkspaceSetupSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadAgentView(APIView):
    """Allows downloading the monitoring telemetry agent."""
    permission_classes = [IsAuthenticated]

    def get(self, request, workspace_id):
        workspace = get_object_or_404(Workspace, id=workspace_id, user=request.user)
        base_dir = os.path.dirname(settings.BASE_DIR)
        agent_path = os.path.join(base_dir, "telemetry-agent", "monitoring-agent.zip")

        logger.info(f"Requested agent download for workspace {workspace_id}. Agent path: {agent_path}")

        if not os.path.exists(agent_path):
            logger.error(f"Agent package not found at {agent_path}")
            return Response({"error": "Agent package not found"}, status=status.HTTP_404_NOT_FOUND)

        response = FileResponse(
            open(agent_path, "rb"),
            as_attachment=True,
            filename="monitoring-agent.zip",
            content_type="application/zip"
        )
        response["Content-Disposition"] = 'attachment; filename="monitoring-agent.zip"'
        return response


class EventIngestView(APIView):
    """Ingests a single telemetry event."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return Response({"error": "API key missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            Workspace.objects.get(api_key=api_key)
        except Workspace.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = request.data.copy()
        payload["api_key"] = api_key
        process_event_task.delay(payload)
        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)


class BatchEventIngestView(APIView):
    """Ingests a batch of telemetry events."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return Response({"error": "API key missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            Workspace.objects.get(api_key=api_key)
        except Workspace.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED)

        events = request.data.get("events", [])
        
        logger.info(f"Received batch event ingest with {len(events)} events.")
        
        for event in events:
            logger.debug(f"Processing event: {event.get('event_type')}")
            event["api_key"] = api_key
            process_event_task.delay(event)
            
        return Response({"accepted": len(events)}, status=status.HTTP_202_ACCEPTED)


class AIInsightsView(APIView):
    """Returns AI insights dashboard data for a workspace."""
    def get(self, request):
        workspace_id = request.GET.get("workspace")
        if not workspace_id:
            return Response({"error": "workspace query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        latest_rca = RootCauseAnalysis.objects.filter(workspace_id=workspace_id).order_by("-created_at").first()
        latest_health_score = HealthScore.objects.filter(workspace_id=workspace_id).order_by("-updated_at").first()
        recommendations = Recommendation.objects.filter(workspace_id=workspace_id).order_by("-created_at")[:5]
        anomalies = Anomaly.objects.filter(workspace_id=workspace_id).order_by("-created_at")[:10]
        insights = RCAInsight.objects.filter(workspace_id=workspace_id).order_by("-occurrence_count")[:2]
        
        alerts_count = Alert.objects.filter(workspace_id=workspace_id, status="OPEN").count()
        anomaly_count = Anomaly.objects.filter(workspace_id=workspace_id).count()
        risk_prediction = RiskPrediction.objects.filter(workspace_id=workspace_id).order_by("-created_at").first()

        return Response({
            "latest_rca": RootCauseAnalysisSerializer(latest_rca).data if latest_rca else None,
            "health_score": HealthScoreSerializer(latest_health_score).data if latest_health_score else None,
            "recommendations": RecommendationSerializer(recommendations, many=True).data,
            "recent_anomalies": AnomalySerializer(anomalies, many=True).data,
            "top_insights": RCAInsightSerializer(insights, many=True).data,
            "alerts_count": alerts_count,
            "anomaly_count": anomaly_count,
            "risk_prediction": RiskPredictionSerializer(risk_prediction).data if risk_prediction else None
        })


class AITrendView(APIView):
    """Returns trending insights data in a structured, enterprise‑grade format."""

    def get(self, request):
        workspace_id = request.GET.get("workspace")
        period = request.GET.get("period", "7d")
        # ---------------------------------------------------------------------
        # Helper: parse period string like "24h", "7d", "30d" into a datetime
        # ---------------------------------------------------------------------
        def parse_period(p: str) -> datetime:
            now = timezone.now()
            if p.endswith("h"):
                hours = int(p.rstrip("h"))
                return now - timedelta(hours=hours)
            if p.endswith("d"):
                days = int(p.rstrip("d"))
                return now - timedelta(days=days)
            # fallback to 7 days
            return now - timedelta(days=7)

        start_time = parse_period(period)
        end_time = timezone.now()

        # ---------------------------------------------------------------------
        # Gather raw data within the period
        # ---------------------------------------------------------------------
        health_hist = HealthScoreHistory.objects.filter(
            workspace_id=workspace_id,
            created_at__range=(start_time, end_time)
        ).order_by("created_at")
        alerts_qs = Alert.objects.filter(
            workspace_id=workspace_id,
            created_at__range=(start_time, end_time)
        ).order_by("created_at")
        anomalies_qs = Anomaly.objects.filter(
            workspace_id=workspace_id,
            created_at__range=(start_time, end_time)
        ).order_by("created_at")
        risk_qs = RiskPrediction.objects.filter(
            workspace_id=workspace_id,
            created_at__range=(start_time, end_time)
        ).order_by("created_at")
        rca_qs = RootCauseAnalysis.objects.filter(
            workspace_id=workspace_id,
            created_at__range=(start_time, end_time)
        ).order_by("created_at")
        # ---------------------------------------------------------------------
        # Single‑node detection
        # ---------------------------------------------------------------------
        node_ids = HealthScore.objects.filter(workspace_id=workspace_id).values_list("node_id", flat=True).distinct()
        single_node = node_ids.count() == 1
        # ---------------------------------------------------------------------
        # Build chart datasets
        # ---------------------------------------------------------------------
        health_score_chart = [
            {"timestamp": hs.created_at.isoformat(), "score": hs.score}
            for hs in health_hist
        ]
        alert_chart = [
            {"timestamp": a.created_at.isoformat(), "count": 1}
            for a in alerts_qs
        ]
        anomaly_chart = [
            {"timestamp": an.created_at.isoformat(), "count": 1}
            for an in anomalies_qs
        ]
        risk_chart = [
            {"timestamp": rp.created_at.isoformat(), "risk_score": rp.risk_score}
            for rp in risk_qs
        ]
        # Stability is derived from health score (higher = more stable)
        stability_chart = [
            {"timestamp": hs.created_at.isoformat(), "stability": hs.score}
            for hs in health_hist
        ]
        # ---------------------------------------------------------------------
        # Pattern distribution – derived dynamically from anomaly metric_names
        # ---------------------------------------------------------------------
        pattern_counts = (
            anomalies_qs.values("metric_name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        pattern_distribution = [
            {"pattern": entry["metric_name"], "count": entry["count"]}
            for entry in pattern_counts
        ]
        # ---------------------------------------------------------------------
        # Metric drift – using TrendSnapshot records (no new tables)
        # ---------------------------------------------------------------------
        metric_drift = []
        snapshots = (
            TrendSnapshot.objects.filter(
                workspace_id=workspace_id,
                created_at__range=(start_time, end_time)
            )
            .order_by("metric_name", "-created_at")
        )
        # Group by metric_name
        from collections import defaultdict
        metric_groups = defaultdict(list)
        for snap in snapshots:
            metric_groups[snap.metric_name].append(snap)
        for metric, snaps in metric_groups.items():
            # latest value
            current = snaps[0].current_value
            # baseline = average of the last N values (N=5 or all within period)
            values = [s.current_value for s in snaps[:5]]
            baseline = sum(values) / len(values) if values else current
            drift_pct = ((current - baseline) / baseline * 100) if baseline != 0 else 0
            metric_drift.append({
                "metric": metric,
                "current": current,
                "baseline": baseline,
                "drift_percentage": round(drift_pct, 2),
            })
        # ---------------------------------------------------------------------
        # Infrastructure timeline – merge ordered events
        # ---------------------------------------------------------------------
        timeline_events = []
        def add_event(ts, event_type, title, severity, node, description):
            timeline_events.append({
                "timestamp": ts.isoformat(),
                "type": event_type,
                "title": title,
                "severity": severity,
                "node": node,
                "description": description,
            })
        
        # Health Score changes (Threshold based)
        last_scores = {}
        for hs in health_hist:
            prev_score = last_scores.get(hs.node_id)
            if prev_score is None:
                last_scores[hs.node_id] = hs.score
            else:
                diff = hs.score - prev_score
                if abs(diff) >= 5: # Threshold for significant change
                    severity = "RECOVERY" if diff > 0 else "MEDIUM"
                    title = "Health Recovered" if diff > 0 else "Health Degraded"
                    desc = f"Health Score changed from {prev_score} to {hs.score}."
                    add_event(hs.created_at, "health", title, severity, hs.node_id, desc)
                    last_scores[hs.node_id] = hs.score

        for a in alerts_qs:
            add_event(a.created_at, "alert", "Alert Triggered", a.severity, a.node_id, a.title)
            
        for an in anomalies_qs:
            add_event(an.created_at, "anomaly", "Anomaly Detected", "WARNING", an.node_id, f"Anomaly in {an.metric_name}. Score: {an.anomaly_score:.2f}")
            
        for rca in rca_qs:
            add_event(rca.created_at, "rca", "Root Cause Generated", "AI Analysis", rca.node_id, rca.summary)
            
        for rp in risk_qs:
            # We don't have historical previous risk level easily without sorting by node, 
            # so we just say Prediction Updated
            add_event(rp.created_at, "risk", "Prediction Updated", "Prediction", rp.node_id, f"Risk Level: {rp.risk_level}. {rp.explanation}")
            
        # Sort chronologically
        timeline_events.sort(key=lambda e: e["timestamp"], reverse=True)
        # ---------------------------------------------------------------------
        # Forecast – reuse risk prediction history (no new forecasting engine)
        # ---------------------------------------------------------------------
        forecast = {
            "risk_evolution": risk_chart,
        }
        # ---------------------------------------------------------------------
        # Summary generation – data‑driven description & executive metrics
        # ---------------------------------------------------------------------
        def generate_summary_and_metrics():
            latest_health = health_hist.last()
            latest_risk = risk_qs.last()
            alert_total = alerts_qs.count()
            anomaly_total = anomalies_qs.count()

            # Basic textual summary
            summary_parts = []
            if latest_health:
                summary_parts.append(f"Current health score is {latest_health.score:.1f}.")
            if latest_risk:
                summary_parts.append(f"Latest risk prediction is {latest_risk.risk_score:.1f} ({latest_risk.risk_level}).")
            summary_parts.append(f"During the selected period there were {alert_total} alerts and {anomaly_total} anomalies.")
            executive_summary = " ".join(summary_parts)

            # Executive metrics calculations
            overall_trend = "Stable"
            if health_score_chart:
                first = health_score_chart[0]["score"]
                last = health_score_chart[-1]["score"]
                if last > first:
                    overall_trend = "Improving"
                elif last < first:
                    overall_trend = "Deteriorating"

            avg_health_score = None
            if health_score_chart:
                avg_health_score = sum(item["score"] for item in health_score_chart) / len(health_score_chart)

            active_anomalies = anomaly_total

            risk_trend = "Stable"
            if risk_chart:
                first_risk = risk_chart[0]["risk_score"]
                last_risk = risk_chart[-1]["risk_score"]
                if last_risk > first_risk:
                    risk_trend = "Increasing"
                elif last_risk < first_risk:
                    risk_trend = "Decreasing"

            stability = "Unknown"
            if latest_health:
                if latest_health.score >= 80:
                    stability = "High"
                elif latest_health.score >= 60:
                    stability = "Moderate"
                else:
                    stability = "Low"

            executive_metrics = {
                "overall_trend": overall_trend,
                "avg_health_score": round(avg_health_score, 2) if avg_health_score is not None else None,
                "active_anomalies": active_anomalies,
                "risk_trend": risk_trend,
                "stability": stability,
                "explanation": executive_summary,
            }
            return executive_summary, executive_metrics

        executive_summary, executive_metrics = generate_summary_and_metrics()
        # ---------------------------------------------------------------------
        # Assemble final response
        # ---------------------------------------------------------------------
        response_data = {
            "summary": {
                "executive": executive_summary,
                "executive_metrics": executive_metrics,
            },
            "single_node": single_node,
            "charts": {
                "health_score": health_score_chart,
                "alerts": alert_chart,
                "anomalies": anomaly_chart,
                "risk": risk_chart,
                "stability": stability_chart,
                "pattern_distribution": pattern_distribution,
            },
            "metric_drift": metric_drift,
            "timeline": timeline_events,
            "forecast": forecast,
            "metadata": {
                "workspace_id": workspace_id,
                "period": period,
                "generated_at": timezone.now().isoformat(),
            },
        }
        return Response(response_data)



class RiskPredictionView(APIView):
    """Returns risk predictions data."""
    def get(self, request):
        workspace_id = request.GET.get("workspace")
        predictions = RiskPrediction.objects.filter(workspace_id=workspace_id).order_by("-risk_score")
        serializer = RiskPredictionSerializer(predictions, many=True)
        return Response(serializer.data)


class AIChatView(APIView):
    """Handles chat interaction with the AI assistant."""
    def post(self, request):
        workspace_id = request.data.get("workspace")
        question = request.data.get("question")

        if not workspace_id:
            return Response({"error": "workspace required"}, status=status.HTTP_400_BAD_REQUEST)
        if not question:
            return Response({"error": "question required"}, status=status.HTTP_400_BAD_REQUEST)

        answer = ask_inframind(workspace_id, question)
        return Response({"answer": answer})