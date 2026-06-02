from celery import shared_task  # type: ignore

from .services import process_event


@shared_task
def process_event_task(event_data):

    process_event(event_data)