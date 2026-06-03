# telemetry-agent/parser.py

from datetime import datetime


def parse_log(service_name,raw_log):

    return {

        "node_id": "local-node",

        "source_service": service_name,

        "event_type": "log",

        "message": raw_log.strip(),

        "raw_log": raw_log.strip(),

        "severity": detect_severity(
            raw_log
        ),

        "metadata": {

            "collected_at": str(
                datetime.utcnow()
            )
        }
    }


def detect_severity(log):

    log = log.upper()

    if "CRITICAL" in log:
        return "CRITICAL"

    if "ERROR" in log:
        return "ERROR"

    if "WARNING" in log:
        return "WARNING"

    return "INFO"