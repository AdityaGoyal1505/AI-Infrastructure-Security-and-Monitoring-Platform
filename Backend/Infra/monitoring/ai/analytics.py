import logging
import math
from datetime import datetime, timedelta
from typing import List, Tuple

from django.db.models import Count, F, Avg
from django.db.models.functions import Abs
from django.utils import timezone

from monitoring.models import Alert, Anomaly, HealthScoreHistory

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _fetch_history(workspace_id: int, node_id: str, limit: int = 50) -> Tuple[List[float], List[datetime]]:
    """Return up to ``limit`` health scores for a node ordered oldest→newest.

    Returns:
        scores: List of health scores (float)
        timestamps: Corresponding list of ``created_at`` datetimes
    """
    # Query newest records up to ``limit`` and reverse to chronological order
    qs = HealthScoreHistory.objects.filter(workspace_id=workspace_id, node_id=node_id)
    qs = qs.order_by("-created_at")[:limit]
    history = list(qs)[::-1]
    scores = [h.score for h in history]
    timestamps = [h.created_at for h in history]

    logger.debug(
        "Fetched %d HealthScoreHistory records for node %s (workspace %d)",
        len(scores),
        node_id,
        workspace_id,
    )
    return scores, timestamps


def _linear_regression_slope(x: List[int], y: List[float]) -> float:
    """Simple linear regression slope (y = a*x + b)."""
    n = len(x)
    if n < 2:
        return 0.0
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi * xi for xi in x)
    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x2 - sum_x * sum_x
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _trend_from_slope(slope: float, std_dev: float) -> str:
    """Map slope and volatility to a human‑readable health trend."""
    if slope >= 8:
        return "Recovering"
    if 3 <= slope < 8:
        return "Improving"
    if slope <= -15:
        return "Rapidly Degrading"
    if -15 < slope <= -5:
        return "Degrading"
    if std_dev > 12:
        return "Highly Volatile"
    return "Stable"


def _standard_deviation(values: List[float]) -> float:
    n = len(values)
    if n == 0:
        return 0.0
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    return math.sqrt(variance)


def _calculate_volatility_penalty(std_dev: float) -> float:
    if std_dev <= 5: return 0.0
    if std_dev <= 10: return 5.0
    if std_dev <= 20: return 10.0
    if std_dev <= 30: return 18.0
    if std_dev <= 40: return 22.0
    return 25.0

def _calculate_alert_penalty(alert_cnt: int) -> float:
    if alert_cnt == 0: return 0.0
    if alert_cnt <= 10: return 2.0
    if alert_cnt <= 30: return 5.0
    if alert_cnt <= 75: return 8.0
    if alert_cnt <= 150: return 12.0
    if alert_cnt <= 300: return 16.0
    return 20.0

def _calculate_anomaly_penalty(anomaly_cnt: int) -> float:
    if anomaly_cnt == 0: return 0.0
    if anomaly_cnt <= 10: return 3.0
    if anomaly_cnt <= 25: return 5.0
    if anomaly_cnt <= 50: return 8.0
    if anomaly_cnt <= 100: return 12.0
    if anomaly_cnt <= 200: return 15.0
    return 20.0

def _stability_score(std_dev: float, alert_cnt: int, recent_anomaly_cnt: int, recent_drop: bool, scores: List[float]) -> float:
    current_health = scores[-1] if scores else 100.0
    health_component = current_health * 0.40
    volatility_penalty = _calculate_volatility_penalty(std_dev)
    volatility_component = max(0.0, 20.0 - (volatility_penalty * 0.8)) # scale 25 max to 20 component
    alert_penalty = _calculate_alert_penalty(alert_cnt)
    alert_component = 20.0 - alert_penalty
    anomaly_penalty = _calculate_anomaly_penalty(recent_anomaly_cnt)
    anomaly_component = 20.0 - anomaly_penalty
    return max(0.0, min(100.0, health_component + volatility_component + alert_component + anomaly_component))

def _confidence_score(sample_cnt: int, std_dev: float, *extra_args, **extra_kwargs) -> int:
    if extra_args or extra_kwargs:
        logger.debug("_confidence_score received extra arguments: args=%s kwargs=%s", extra_args, extra_kwargs)
    if sample_cnt <= 2: base = 40
    elif sample_cnt <= 10: base = 80
    elif sample_cnt <= 50: base = 95
    else: base = 99
    volatility_adjust = max(0, int((std_dev - 10) * 0.5))
    return max(10, min(99, base - volatility_adjust))

def _stability_label(score: float) -> str:
    if score >= 95: return f"{int(score)} (Excellent)"
    if score >= 85: return f"{int(score)} (Very Stable)"
    if score >= 70: return f"{int(score)} (Stable)"
    if score >= 55: return f"{int(score)} (Moderate)"
    if score >= 35: return f"{int(score)} (Unstable)"
    return f"{int(score)} (Critical)"

def _exponential_smoothing(values: List[float], alpha: float = 0.3, steps: int = 6) -> List[float]:
    if not values: return [0.0] * steps
    s = values[0]
    for v in values[1:]:
        s = alpha * v + (1 - alpha) * s
    slope = (values[-1] - values[0]) / max(1, len(values) - 1)
    forecast = []
    for i in range(1, steps + 1):
        proj = s + slope * i
        proj = max(0.0, min(100.0, proj))
        forecast.append(round(proj, 1))
    return forecast

def _failure_window(forecast: List[float], critical_threshold: float = 20.0) -> str:
    for idx, val in enumerate(forecast, start=1):
        if val <= critical_threshold: return f"{idx} Hours"
    return "No predicted failure"

def _incident_probability(trend: str, current_health: float, alert_cnt: int, anomaly_cnt: int) -> int:
    base = 0.0
    if trend == "Rapidly Degrading": base += 40
    elif trend == "Degrading": base += 25
    elif trend == "Highly Volatile": base += 15
    
    if current_health < 50:
        base += (50 - current_health) * 0.8
        
    alert_factor = min(30, alert_cnt * 0.15)
    anomaly_factor = min(30, anomaly_cnt * 0.15)
    base += alert_factor + anomaly_factor
    
    if trend == "Recovering":
        base = base * 0.4
    elif trend == "Improving":
        base = base * 0.7
        
    if base < 5:
        base = 5 + (alert_cnt * 0.05)
        
    return min(100, max(5, int(base)))


# Removed duplicate _confidence_score; using robust version defined earlier.

# ---------------------------------------------------------------------------
# Public analytics functions
# ---------------------------------------------------------------------------

def get_node_analytics(workspace_id: int, node_id: str) -> dict:
    """Compute analytics for a node using HealthScoreHistory only.

    Returns exactly the keys expected by the frontend.
    """
    now = timezone.now()
    past_7d = now - timedelta(days=7)

    scores, _ = _fetch_history(workspace_id, node_id, limit=50)

    if not scores:
        return {
            "health_trend": "Stable",
            "stability_index": "0 (Critical)",
            "stability_score": 0,
            "incident_probability": "0%",
            "anomaly_frequency": 0,
            "alert_frequency": 0,
            "estimated_failure_window": "No predicted failure",
            "forecast_data": [],
            "confidence_score": 10,
            "confidence_reason": "No historical data available.",
            "current_score": None,
            "previous_score": None,
            "trend_slope": 0,
            "volatility": 0,
        }

    current_score = scores[-1]
    previous_score = scores[-2] if len(scores) >= 2 else current_score
    slope = _linear_regression_slope(list(range(len(scores))), scores)
    std_dev = _standard_deviation(scores)
    recent_drop = len(scores) >= 2 and (scores[-2] - scores[-1]) >= 20

    trend = _trend_from_slope(slope, std_dev)

    from django.conf import settings
    recent_window_hours = getattr(settings, "ANALYTICS_RECENT_WINDOW_HOURS", 24)
    recent_window = now - timedelta(hours=recent_window_hours)

    anomaly_cnt = (
        Anomaly.objects.filter(
            workspace_id=workspace_id,
            node_id=node_id,
            created_at__gte=recent_window,
        )
        .aggregate(cnt=Count("id"))
        .get("cnt")
        or 0
    )
    alert_cnt = (
        Alert.objects.filter(
            workspace_id=workspace_id,
            node_id=node_id,
            status="OPEN",
        )
        .aggregate(cnt=Count("id"))
        .get("cnt")
        or 0
    )

    stability = _stability_score(std_dev, alert_cnt, anomaly_cnt, recent_drop, scores)
    stability_index = _stability_label(stability)

    forecast = _exponential_smoothing(scores, alpha=0.3, steps=6)
    failure_window = _failure_window(forecast)
    incident_prob = _incident_probability(trend, current_score, alert_cnt, anomaly_cnt)
    incident_probability = f"{incident_prob}%"
    confidence = _confidence_score(len(scores), std_dev, alert_cnt, anomaly_cnt)
    confidence_reason = (
        f"Based on {len(scores)} health records, {alert_cnt} alerts, "
        f"{anomaly_cnt} anomalies, and a standard deviation of {std_dev:.1f}."
    )
    return {
        "health_trend": trend,
        "stability_index": stability_index,
        "stability_score": round(stability, 2),
        "incident_probability": incident_probability,
        "anomaly_frequency": anomaly_cnt,
        "alert_frequency": alert_cnt,
        "estimated_failure_window": failure_window,
        "forecast_data": forecast,
        "confidence_score": confidence,
        "confidence_reason": confidence_reason,
        "current_score": current_score,
        "previous_score": previous_score,
        "trend_slope": round(slope, 2),
        "volatility": round(std_dev, 2),
    }

def get_workspace_analytics(workspace_id: int) -> dict:
    """Workspace‑level analytics – improved but backward compatible."""
    now = timezone.now()
    past_7d = now - timedelta(days=7)

    from django.conf import settings
    recent_window_hours = getattr(settings, "ANALYTICS_RECENT_WINDOW_HOURS", 24)
    recent_window = now - timedelta(hours=recent_window_hours)

    anomalies_qs = (
        Anomaly.objects.filter(workspace_id=workspace_id, created_at__gte=recent_window)
        .values("node_id")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )
    most_affected_nodes = [
        {"node_id": a["node_id"], "anomaly_count": a["count"]} for a in anomalies_qs
    ]

    drift_analysis = {}
    for node in most_affected_nodes:
        nid = node["node_id"]
        drift = (
            Anomaly.objects.filter(workspace_id=workspace_id, node_id=nid)
            .annotate(drift=Abs(F("observed_value") - F("baseline_value")))
            .aggregate(avg=Avg("drift"))
            .get("avg")
        )
        drift_analysis[nid] = round(drift or 0, 2)

    node_hist_qs = (
        HealthScoreHistory.objects.filter(workspace_id=workspace_id)
        .values("node_id")
        .annotate(samples=Count("id"))
        .order_by("-samples")[:20]
    )
    stability_scores = []
    for entry in node_hist_qs:
        nid = entry["node_id"]
        scores = list(
            HealthScoreHistory.objects.filter(workspace_id=workspace_id, node_id=nid)
            .order_by("-created_at")[:20]
            .values_list("score", flat=True)
        )
        if not scores:
            continue
        std = _standard_deviation(scores)
        alerts = (
            Alert.objects.filter(
                workspace_id=workspace_id, node_id=nid, status="OPEN"
            )
            .count()
        )
        anomalies = (
            Anomaly.objects.filter(
                workspace_id=workspace_id, node_id=nid, created_at__gte=recent_window
            )
            .count()
        )
        stability_scores.append(_stability_score(std, alerts, anomalies, recent_drop=False, scores=scores))

    overall_stability = (
        round(sum(stability_scores) / len(stability_scores), 2) if stability_scores else 0
    )

    return {
        "most_affected_nodes": most_affected_nodes,
        "metric_drift": drift_analysis,
        "overall_stability": overall_stability,
        "average_node_stability": overall_stability,
        "node_count_with_history": len(node_hist_qs),
    }
