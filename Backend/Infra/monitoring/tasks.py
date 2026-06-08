from celery import shared_task  # type: ignore

from .services import process_event
from .models import Workspace

from .ai.root_cause_engine import generate_root_cause

@shared_task
def process_event_task(event_data):
    process_event(event_data)

@shared_task
def generate_root_cause_task(workspace_id,node_id):

    workspace = Workspace.objects.get(id=workspace_id)

    generate_root_cause(workspace,node_id)