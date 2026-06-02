from django.utils import timezone

from .models import Workspace,Event,NodeStatus


def detect_severity(
    message
):

    message = message.lower()

    if any(

        keyword in message

        for keyword in [

            "critical",
            "fatal",
            "panic"
        ]
    ):

        return "CRITICAL"

    if any(

        keyword in message

        for keyword in [

            "error",
            "failed",
            "exception"
        ]
    ):

        return "ERROR"

    if any(

        keyword in message

        for keyword in [

            "warning",
            "warn"
        ]
    ):

        return "WARNING"

    return "INFO"


def calculate_anomaly_score(
    severity
):

    mapping = {

        "INFO": 0.1,

        "WARNING": 0.4,

        "ERROR": 0.7,

        "CRITICAL": 1.0
    }

    return mapping.get(
        severity,
        0.1
    )


def extract_metadata(
    payload
):

    return payload.get(
        "metadata",
        {}
    )


def process_event(
    event_data
):

    api_key = event_data.get(
        "api_key"
    )

    workspace = Workspace.objects.get(
        api_key=api_key
    )

    event_type = event_data.get(
        "event_type",
        "log"
    )

    node_id = event_data.get(
        "node_id",
        "local-node"
    )

    source_service = event_data.get(
        "source_service",
        "unknown"
    )

    metadata = event_data.get(
        "metadata",
        {}
    )

    if event_type in [

        "metric",
        "heartbeat"

    ]:

        NodeStatus.objects.update_or_create(

            workspace=workspace,

            node_id=node_id,

            defaults={

                "source_service":
                source_service,

                "status":
                "online",

                "cpu_usage":
                metadata.get(
                    "cpu_usage",
                    0
                ),

                "memory_usage":
                metadata.get(
                    "memory_usage",
                    0
                ),

                "disk_usage":
                metadata.get(
                    "disk_usage",
                    0
                ),

                "network_usage":
                metadata.get(
                    "network_usage",
                    0
                ),

                "process_count":
                metadata.get(
                    "process_count",
                    0
                ),

                "agent_version":
                metadata.get(
                    "agent_version",
                    "1.0.0"
                ),

                "last_heartbeat":
                timezone.now(),

                "metadata":
                metadata
            }
        )

        return

    message = event_data.get(
        "message",
        ""
    )

    severity = event_data.get(
        "severity"
    )

    if not severity:

        severity = detect_severity(
            message
        )

    Event.objects.create(

        workspace=workspace,

        node_id=node_id,

        source_service=source_service,

        event_type=event_data.get(
            "event_type",
            "log"
        ),

        severity=severity,

        message=message,

        raw_log=event_data.get(
            "raw_log",
            ""
        ),

        metadata=metadata,

        anomaly_score=
        calculate_anomaly_score(
            severity
        )
    )