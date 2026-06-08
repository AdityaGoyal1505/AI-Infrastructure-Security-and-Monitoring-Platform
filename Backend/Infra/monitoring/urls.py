from django.urls import path

from .views import EventIngestView,BatchEventIngestView

urlpatterns = [

    path("events/ingest/",EventIngestView.as_view()),

    path("events/batch/",BatchEventIngestView.as_view()),
]