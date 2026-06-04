from django.contrib import admin

from .models import (
    User,
    Workspace,
    Event,
    NodeStatus,
    Rule,
    RuleMatch
)

admin.site.register(Rule)

admin.site.register(RuleMatch)
admin.site.register(User)
admin.site.register(Workspace)
admin.site.register(Event)
admin.site.register(NodeStatus)