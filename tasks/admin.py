from django.contrib import admin

from .models import (
    TypeTask,
    Task,
)

admin.site.register(TypeTask)
admin.site.register(Task)
