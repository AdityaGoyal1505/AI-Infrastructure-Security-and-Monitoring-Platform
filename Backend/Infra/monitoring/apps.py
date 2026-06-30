from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    name = 'monitoring'

    def ready(self):
        # Import signal handlers to ensure they are registered
        from . import signals  # noqa: F401


class MonitoringConfig(AppConfig):
    name = 'monitoring'
