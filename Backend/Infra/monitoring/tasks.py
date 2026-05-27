from celery import shared_task #type: ignore

from .models import Event
from .services import (
    detect_severity,
    calculate_anomaly_score,
    extract_metadata,
)


@shared_task
def process_event(event_id):

    try:

        event = Event.objects.get(
            id=event_id
        )

        severity = detect_severity(
            event.raw_log
        )

        anomaly_score = calculate_anomaly_score(
            event.raw_log
        )

        metadata = extract_metadata(
            event.raw_log
        )

        event.severity = severity

        event.anomaly_score = anomaly_score

        event.metadata = metadata

        event.save()

        return (
            f"Processed event {event.id}"
        )

    except Event.DoesNotExist:

        return "Event not found"