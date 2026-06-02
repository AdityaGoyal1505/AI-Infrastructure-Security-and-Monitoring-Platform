import psutil
from datetime import datetime


def collect_system_metrics():

    return {

        "node_id": "local-node",

        "source_service": "system-monitor",

        "event_type": "metric",

        "severity": "INFO",

        "message": "System metrics snapshot",

        "raw_log": "SYSTEM_METRICS",

        "metadata": {

            "cpu_usage": psutil.cpu_percent(),

            "memory_usage": psutil.virtual_memory().percent,

            "disk_usage": psutil.disk_usage('/').percent,

            "network_sent": (
                psutil.net_io_counters().bytes_sent
            ),

            "network_received": (
                psutil.net_io_counters().bytes_recv
            ),

            "timestamp": str(
                datetime.now()
            )
        }
    }