from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # type:ignore

from .views import (
    EventIngestView,
    BatchEventIngestView,
    AIInsightsView,
    AITrendView,
    RiskPredictionView,
    RegisterView,
    LoginView,
    CurrentUserView,
    WorkspaceListCreateView,
    WorkspaceDetailView,
    WorkspaceSetupView,
    DownloadAgentView,
    AIChatView,
    CookieTokenRefreshView
)

urlpatterns = [
    # Authentication Endpoints
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", CurrentUserView.as_view(), name="current-user"),
    path("auth/refresh/", CookieTokenRefreshView.as_view(), name="cookie_refresh"),

    # Workspace Endpoints
    path("workspaces/", WorkspaceListCreateView.as_view(), name="workspace-list-create"),
    path("workspaces/<int:workspace_id>/", WorkspaceDetailView.as_view(), name="workspace-detail"),
    path("workspaces/<int:workspace_id>/setup/", WorkspaceSetupView.as_view(), name="workspace-setup"),
    path("workspaces/<int:workspace_id>/agent/", DownloadAgentView.as_view(), name="download-agent"),

    # Event Ingestion Endpoints
    path("events/ingest/", EventIngestView.as_view(), name="event-ingest"),
    path("events/batch/", BatchEventIngestView.as_view(), name="batch-event-ingest"),

    # AI Insights Endpoints
    path("ai/insights/", AIInsightsView.as_view(), name="ai-insights"),
    path("ai/trends/", AITrendView.as_view(), name="ai-trends"),
    path("ai/predictions/", RiskPredictionView.as_view(), name="ai-predictions"),
    path("ai/chat/", AIChatView.as_view(), name="ai-chat"),
]