from django import forms
from users.models import Developer
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from projects.models import Project

from .models import (
    TypeTask,
    Task,
    Activities,
)


class TypeTaskForm(ModelForm):
    class Meta:
        model = TypeTask
        fields = (
            'name', 'status',
        )
        labels = {
            'name': 'Nombre del tipo del proyecto',
            'status': 'Estado',
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
            'developer', 'description', 'state'
        )
        labels = {
            'developer': 'Desarrolladores',
            'description': 'Descripcion',
            'state': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developer'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['state'].widget.attrs.update({
            'id': 'state_check',
        })


class ActivitiesForm(ModelForm):
    class Meta:
        model = Activities
        fields = (
            'name', 'process',
        )
        labels = {
            'name': 'Nombre',
            'proccess': 'Proceso',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })


TaskFormSet = inlineformset_factory(
    Task, Activities, form=ActivitiesForm,
    fields=['name', 'process'], extra=1, can_delete=True
)
