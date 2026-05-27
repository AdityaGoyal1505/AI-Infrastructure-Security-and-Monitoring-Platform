from django.urls import path #type: ignore
from .views import register_user,create_workspace,ingest_event,health_check

urlpatterns = [

    path(
        'register/',
        register_user
    ),

    path(
        'workspaces/create/',
        create_workspace
    ),

    path(
        'events/ingest/',
        ingest_event
    ),

    path(
        'health/',
        health_check
    ),
]