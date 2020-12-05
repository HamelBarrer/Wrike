from django.contrib import admin

from tasks.models import Task

from .models import Project


class TaskInline(admin.TabularInline):
    model = Task
    fields = ('type_task', 'task',)
    extra = 1


@admin.register(Project)
class ProjectCustom(admin.ModelAdmin):
    fields = ('name', 'developer', 'status', 'porcent')
    list_display = ('name', 'status', 'created_at', 'update_at')
    list_filter = ('status',)
    inlines = (TaskInline,)
