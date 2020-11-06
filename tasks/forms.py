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
        labels = {
            'name': 'Nombre',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = (
            'developer', 'type_task', 'task', 'description', 'state',
        )
        labels = {
            'developer': 'Desarrollador',
            'type_task': 'Tipo de tarea',
            'task': 'Tarea',
            'description': 'Descripcion',
            'state': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developer'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['type_task'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['task'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['state'].widget.attrs.update({
            'class': 'form-check-input',
        })
