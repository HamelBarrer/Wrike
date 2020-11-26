from django.contrib import admin

from .models import (
    TypeTask,
    Task,
    Activities,
)


class ActivitiesInline(admin.TabularInline):
    model = Activities
    extra = 1


@admin.register(TypeTask)
class TypeTaskCustom(admin.ModelAdmin):
    fields = ('name',)
    search_fields = ('name',)
    list_display = ('name', 'created_at')


@admin.register(Task)
class TaskCustom(admin.ModelAdmin):
    fields = ('developer', 'description', 'state')
    search_fields = ['developer__user__username', 'task']
    list_display = ('type_task', 'task', 'description',
                    'state', 'project', 'created_at', 'updated_at')
    list_filter = (
        'developer__user__username',
        'type_task',
        'state',
    )
    inlines = [ActivitiesInline]
