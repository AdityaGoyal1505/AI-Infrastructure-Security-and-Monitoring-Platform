import psutil
from datetime import datetime


def collect_system_metrics(node_id=None):
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

        "source_service": "system-monitor",

        "event_type": "metric",

        "severity": "INFO",

        "message": "System metrics snapshot",

        "raw_log": "SYSTEM_METRICS",

        "metadata": {

            "cpu_usage": psutil.cpu_percent(),

            "memory_usage": psutil.virtual_memory().percent,

            "disk_usage": psutil.disk_usage('/').percent,

            "network_sent": (psutil.net_io_counters().bytes_sent),

            "network_received": (psutil.net_io_counters().bytes_recv),

            "timestamp": str(datetime.now())
        }
    }