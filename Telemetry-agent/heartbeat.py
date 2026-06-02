import socket
import platform

from datetime import datetime


def generate_heartbeat():

    return {

        "node_id": socket.gethostname(),

        "source_service": (
            "telemetry-agent"
        ),

        "event_type": "heartbeat",

        "severity": "INFO",

        "message": (
            "Agent heartbeat active"
        ),

        "raw_log": "HEARTBEAT",

        "metadata": {

            "hostname": (
                socket.gethostname()
            ),

            "os": platform.system(),

            "platform": platform.platform(),

            "timestamp": str(
                datetime.now()
            )
        }
    }