from django import forms
from django.forms import ModelForm

from .models import (
    TypeTask,
    Task,
    Activities,
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
            'developer', 'type_task', 'task','description', 'state',
        )
        labels = {
            'developer': 'Desarrollador',
            'type_task': 'Tipo de tarea',
            'task': 'Tarea',
            'description': 'Descripcion',
            'state': 'Estado',
            # 'project_start': 'Fecha de Inicio',
            # 'project_finished': 'Fecha de Finalizacion',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developer'].widget.attrs.update({
            'id': 'developer_id',
            'class': 'form-control',
        })
        self.fields['type_task'].widget.attrs.update({
            'id': 'type_task_id',
            'class': 'form-control',
        })
        self.fields['task'].widget.attrs.update({
            'id': 'task_id',
            'class': 'form-control',
        })
        self.fields['description'].widget.attrs.update({
            'id': 'description_id',
            'class': 'form-control',
        })
        self.fields['state'].widget.attrs.update({
            'id': 'state_id',
            'class': 'form-check-input',
        })


class ActivitiesForm(ModelForm):
    class Meta:
        model = Activities
        fields = (
            'name',
        )