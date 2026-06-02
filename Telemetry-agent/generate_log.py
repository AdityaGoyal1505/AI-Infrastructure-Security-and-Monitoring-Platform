# telemetry-agent/generate_logs.py

import os
import random
import time
from datetime import datetime


LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


SERVICES = {

    "redis": [

        "[INFO] Redis connection established",
        "[INFO] Cache hit CPU={cpu} MEMORY={memory}",
        "[WARNING] Memory spike MEMORY={memory}",
        "[ERROR] Redis timeout CPU={cpu} MEMORY={memory}",
        "[CRITICAL] Redis unavailable CPU={cpu} MEMORY={memory}",

        "[METRIC] CPU={cpu} MEMORY={memory} DISK={disk} NETWORK={network}",

        "[METRIC] LATENCY={latency} CPU={cpu} MEMORY={memory}",
    ],

    "celery": [

        "[INFO] Celery worker started",
        "[WARNING] Queue backlog increasing",
        "[ERROR] Task timeout CPU={cpu}",
        "[CRITICAL] Worker crashed MEMORY={memory}",

        "[METRIC] CPU={cpu} MEMORY={memory} DISK={disk}",

        "[METRIC] NETWORK={network} LATENCY={latency}",
    ],

    "django": [

        "[INFO] GET /api/events/ 200 OK",
        "[WARNING] Suspicious login detected",
        "[ERROR] Internal Server Error CPU={cpu}",
        "[CRITICAL] DB pool exhausted MEMORY={memory}",

        "[METRIC] CPU={cpu} MEMORY={memory} LATENCY={latency}",

        "[METRIC] NETWORK={network} DISK={disk}",
    ],

    "postgres": [

        "[INFO] Query executed",
        "[WARNING] Slow query LATENCY={latency}",
        "[ERROR] Deadlock detected CPU={cpu}",
        "[CRITICAL] Replication failure MEMORY={memory}",

        "[METRIC] CPU={cpu} MEMORY={memory} DISK={disk}",

        "[METRIC] NETWORK={network}",
    ],

    "react": [

        "[INFO] Dashboard rendered",
        "[WARNING] Re-render spike",
        "[ERROR] API fetch failed CPU={cpu}",
        "[CRITICAL] Frontend crash MEMORY={memory}",

        "[METRIC] LATENCY={latency} CPU={cpu}",

        "[METRIC] MEMORY={memory} NETWORK={network}",
    ]
}


def rand():

    return random.randint(20, 100)


def latency():

    return random.randint(100, 5000)


def network():

    return random.randint(
        1000,
        100000
    )


def generate_log(template):

    return template.format(

        cpu=rand(),

        memory=rand(),

        disk=rand(),

        network=network(),

        latency=latency()
    )


def write_logs(
    service_name,
    templates
):

    file_path = os.path.join(
        LOG_DIR,
        f"{service_name}.log"
    )

    with open(file_path, "a") as log_file:

        for _ in range(100):

            template = random.choice(
                templates
            )

            log_message = generate_log(
                template
            )

            timestamp = datetime.utcnow(
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            final_log = (
                f"{timestamp} "
                f"{log_message}\n"
            )

            log_file.write(
                final_log
            )

            print(
                f"[{service_name.upper()}] "
                f"{final_log.strip()}"
            )

            time.sleep(
                random.uniform(
                    0.05,
                    0.2
                )
            )


def main():

    for (
        service_name,
        templates
    ) in SERVICES.items():

        write_logs(
            service_name,
            templates
        )

    print(
        "\nTelemetry logs generated."
    )


if __name__ == "__main__":

    main()