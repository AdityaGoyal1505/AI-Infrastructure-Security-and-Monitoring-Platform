import os
import sys
import json
import time
import threading

from watcher import start_watcher
from heartbeat import generate_heartbeat
from metrics_collector import collect_system_metrics
from process_monitor import collect_process_metrics
from batch_sender import batch_sender_loop
from event_queue import event_queue
from config_validator import validate_config


BASE_DIR = os.path.dirname(
    sys.executable
) if getattr(
    sys,
    "frozen",
    False
) else os.path.dirname(
    os.path.abspath(__file__)
)

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "config.json"
)

with open(
    CONFIG_PATH,
    "r"
) as config_file:

    config = json.load(
        config_file
    )

validate_config(config)

backend_url = config[
    "backend_url"
]

api_key = config[
    "api_key"
]


def metrics_loop():

    while True:

        try:

            metrics_event = (
                collect_system_metrics()
            )

            event_queue.put(
                metrics_event
            )

            process_event = (
                collect_process_metrics()
            )

            event_queue.put(
                process_event
            )

        except Exception as error:

            print(
                f"[METRICS ERROR] "
                f"{error}"
            )

        time.sleep(10)


def heartbeat_loop():

    while True:

        try:

            heartbeat = (
                generate_heartbeat()
            )

            event_queue.put(
                heartbeat
            )

        except Exception as error:

            print(
                f"[HEARTBEAT ERROR] "
                f"{error}"
            )

        time.sleep(60)


if __name__ == "__main__":

    print(
        "[STARTING] "
        "Telemetry Agent"
    )

    threads = []

    for log_config in config["logs"]:

        thread = threading.Thread(

            target=start_watcher,

            args=(

                log_config["service"],

                log_config["path"],

                backend_url,

                api_key
            ),

            daemon=True
        )

        thread.start()

        threads.append(
            thread
        )

    metrics_thread = threading.Thread(

        target=metrics_loop,

        daemon=True
    )

    metrics_thread.start()

    threads.append(
        metrics_thread
    )

    heartbeat_thread = threading.Thread(

        target=heartbeat_loop,

        daemon=True
    )

    heartbeat_thread.start()

    threads.append(
        heartbeat_thread
    )

    batch_thread = threading.Thread(

        target=batch_sender_loop,

        args=(

            backend_url,

            api_key
        ),

        daemon=True
    )

    batch_thread.start()

    threads.append(
        batch_thread
    )

    print(
        "[RUNNING] "
        "Agent active"
    )

    while True:

        time.sleep(5)