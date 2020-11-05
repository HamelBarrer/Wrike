from django.forms import ModelForm

from .models import (
    TypeTask,
    Task,
)


class TypeTaskForm(ModelForm):
    class Meta:
        model = TypeTask
        fields = (
            'name',
        )


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = (
            'user', 'type_task', 'task', 'description', 'state',
        )
