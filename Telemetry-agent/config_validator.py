import os


def validate_config(config):

    required_fields = [
        "backend_url",
        "api_key",
        "logs"
    ]

    for field in required_fields:

        if field not in config:

            raise ValueError(
                f"Missing field: {field}"
            )

    for log in config["logs"]:

        if not os.path.exists(
            log["path"]
        ):

            print(
                f"Warning: {log['path']} "
                "does not exist"
            )