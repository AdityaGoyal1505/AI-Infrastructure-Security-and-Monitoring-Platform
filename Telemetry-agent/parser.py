# telemetry-agent/parser.py

from datetime import datetime
import re

def parse_log(service_name, raw_log):

    metadata = {"collected_at":str(datetime.utcnow())}

    event_type = "log"

    if "[METRIC]" in raw_log.upper():

        event_type = "metric"

        matches = re.findall(
            r'([A-Z_]+)=([0-9.]+)',
            raw_log.upper()
        )

        for key, value in matches:

            value = float(value)

            mapping = {

                "CPU":"cpu_usage",

                "MEMORY":"memory_usage",

                "DISK":"disk_usage",

                "NETWORK":"network_usage",

                "CONNECTIONS":"db_connections",

                "DB_CPU":"db_cpu_usage",

                "DB_MEMORY":"db_memory_usage",

                "LATENCY":"api_latency"
            }

            metadata[mapping.get(key,key.lower())] = value

    return {

        "node_id":"local-node",

        "source_service":service_name,

        "event_type":event_type,

        "message":raw_log.strip(),

        "raw_log":raw_log.strip(),

        "severity":detect_severity(raw_log),

        "metadata":metadata
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