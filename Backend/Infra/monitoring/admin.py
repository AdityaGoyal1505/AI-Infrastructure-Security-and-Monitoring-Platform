from django.contrib import admin

from .models import (
    Anomaly,
    User,
    Workspace,
    Event,
    NodeStatus,
    Rule,
    RuleMatch,
    Alert,
    HealthScore,
    Correlation,
)
admin.site.register(Correlation)
admin.site.register(HealthScore)
admin.site.register(Rule)
admin.site.register(Anomaly)
admin.site.register(Alert)
admin.site.register(RuleMatch)
admin.site.register(User)
admin.site.register(Workspace)
admin.site.register(Event)
admin.site.register(NodeStatus)