from django.contrib import admin

from .models import (
    User,
    Workspace,
    Event,
    NodeStatus
)


admin.site.register(User)
admin.site.register(Workspace)
admin.site.register(Event)
admin.site.register(NodeStatus)