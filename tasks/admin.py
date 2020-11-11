from django.contrib import admin

from .models import (
    TypeTask,
    Task,
    Activities
)

class ActivitiesInline(admin.TabularInline):
    model = Activities
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [ActivitiesInline]

admin.site.register(TypeTask)
admin.site.register(Task, TaskAdmin)
