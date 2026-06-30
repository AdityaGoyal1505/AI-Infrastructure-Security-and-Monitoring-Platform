import psutil

from datetime import datetime


def collect_process_metrics(node_id="local-node"):

    process_count = len(list(psutil.process_iter()))

    failed_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'status']):

        try:

            if proc.info['status'] == 'zombie':

                failed_processes.append(proc.info['name'])

        except Exception:

            continue

    return {

        "node_id": node_id,

        "source_service": ("process-monitor"),

        "event_type": "metric",

        "severity": ("WARNING" if failed_processes else "INFO"),

        "message": ("Process monitoring snapshot"),

        "raw_log": "PROCESS_METRICS",

        "metadata": {

            "process_count": (process_count),

            "failed_processes": (failed_processes),

            "timestamp": str(datetime.now())
        }
    }