import time
import requests

from event_queue import event_queue


def start_api_monitor(api_config):

    while True:

        try:

            start_time = time.time()

            response = requests.request(
                method=api_config.get("method", "GET"),
                url=api_config["url"],
                timeout=api_config.get("timeout", 5)
            )

            latency_ms = round(
                (time.time() - start_time) * 1000,
                2
            )

            severity = (
                "ERROR"
                if response.status_code >= 500
                else "INFO"
            )

            event_queue.put({

                "node_id": "local-node",

                "source_service":
                api_config["service"],

                "event_type":
                "metric",

                "severity":
                severity,

                "message":
                f"API returned {response.status_code}",

                "raw_log":
                api_config["url"],

                "metadata": {

                    "status_code":
                    response.status_code,

                    "latency_ms":
                    latency_ms
                }
            })

        except Exception as error:

            event_queue.put({

                "node_id": "local-node",

                "source_service":
                api_config["service"],

                "event_type":
                "log",

                "severity":
                "CRITICAL",

                "message":
                str(error),

                "raw_log":
                api_config["url"],

                "metadata": {}
            })

        time.sleep(
            api_config.get(
                "interval",
                10
            )
        )