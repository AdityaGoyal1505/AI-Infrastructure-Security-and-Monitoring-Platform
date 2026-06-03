from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Workspace

from .tasks import process_event_task

class EventIngestView(APIView):
# ac5b2164-c5a3-4ff8-8806-9621cc78807e
    authentication_classes = []
    permission_classes = []

    def post(
        self,
        request
    ):

        api_key = request.headers.get(
            "X-API-KEY"
        )

        if not api_key:

            return Response(

                {
                    "error":
                    "API key missing"
                },

                status=401
            )

        try:

            Workspace.objects.get(
                api_key=api_key
            )

        except Workspace.DoesNotExist:

            return Response(

                {
                    "error":
                    "Invalid API key"
                },

                status=401
            )

        payload = request.data.copy()

        payload["api_key"] = api_key

        process_event_task.delay(
            payload
        )

        return Response(

            {
                "status":
                "accepted"
            },

            status=202
        )


class BatchEventIngestView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(
        self,
        request
    ):

        api_key = request.headers.get(
            "X-API-KEY"
        )

        if not api_key:

            return Response(

                {
                    "error":
                    "API key missing"
                },

                status=401
            )

        try:

            Workspace.objects.get(
                api_key=api_key
            )

        except Workspace.DoesNotExist:

            return Response(

                {
                    "error":
                    "Invalid API key"
                },

                status=401
            )

        events = request.data.get(
            "events",
            []
        )
        for event in events:
            print("RECEIVED EVENT")
            print(event)
            print("TYPE:", event.get("event_type"))

            event["api_key"] = api_key
            process_event_task.delay(event)
        return Response(

            {
                "accepted":
                len(events)
            },

            status=202
        )