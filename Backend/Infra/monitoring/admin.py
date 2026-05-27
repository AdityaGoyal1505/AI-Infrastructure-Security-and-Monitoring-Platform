from django.contrib import admin #type: ignore

# Register your models here.

from .models import User,Workspace,Event


admin.site.register(User)

admin.site.register(Workspace)

admin.site.register(Event)