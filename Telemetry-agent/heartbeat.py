import socket
import platform

from datetime import datetime


def generate_heartbeat(node_id=None):
    # Load node_id from config if not supplied
    if node_id is None:
        import os, sys, json
        BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
        try:
            with open(CONFIG_PATH, "r") as cfg_file:
                cfg = json.load(cfg_file)
                node_id = cfg.get("node_id", "local-node")
        except Exception:
            node_id = "local-node"
    return {

        "node_id": node_id,

        "source_service": ("telemetry-agent"),

        "event_type": "heartbeat",

        "severity": "INFO",

        "message": ("Agent heartbeat active"),

        "raw_log": "HEARTBEAT",

        "metadata": {

            "hostname": (socket.gethostname()),

            "os": platform.system(),

            "platform": platform.platform(),

            "timestamp": str(datetime.now())
        }
    }