from django.contrib import admin

from .models import (
    TypeTask,
    Task,
    Activities,
)

admin.site.register(Task)
admin.site.register(Activities)
