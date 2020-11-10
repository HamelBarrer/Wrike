from django.contrib import admin

from .models import (
    TypeTask,
    Task,
    Activities,
    ActivitiesTasks,
)

admin.site.register(TypeTask)
admin.site.register(Task)
admin.site.register(Activities)
admin.site.register(ActivitiesTasks)
