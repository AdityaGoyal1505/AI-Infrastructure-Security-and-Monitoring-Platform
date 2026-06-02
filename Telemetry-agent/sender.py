# telemetry-agent/sender.py

import requests


def send_batch(backend_url,api_key,events):

    headers = {

        "X-API-KEY": api_key,

        "Content-Type":
        "application/json"
    }

    try:

        response = requests.post(

            backend_url,

            json={
                "events": events
            },

            headers=headers,

            timeout=15
        )

        if response.status_code in [

            200,
            201,
            202

        ]:

            print(

                f"[BATCH SUCCESS] "
                f"{len(events)} "
                f"events sent"
            )

            return True

        print(

            f"[BATCH FAILED] "
            f"{response.status_code}"
        )

        return False

    except Exception as error:

        print(

            f"[BATCH ERROR] "
            f"{error}"
        )

        return False


def send_event(backend_url,api_key,event_data):

    headers = {

        "X-API-KEY": api_key,

        "Content-Type":
        "application/json"
    }

    try:

        response = requests.post(

            backend_url,

            json=event_data,

            headers=headers,

            timeout=10
        )

        if response.status_code in [
            200,
            201,
            202

        ]:

            print(

                f"[SUCCESS] "
                f"{event_data.get('event_type')} "
                f"sent"
            )

            return True

        print(

            f"[FAILED] "
            f"{response.status_code}"
        )

        return False

    except Exception as error:

        print(

            f"[SEND ERROR] "
            f"{error}"
        )

        return False