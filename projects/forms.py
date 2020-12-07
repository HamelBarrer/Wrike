from tasks.models import TypeTask
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tasks.forms import Task

from users.models import User

from .models import Project


class ProjectForm(ModelForm):
    developer = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name='desarrolladores'))

    class Meta:
        model = Project
        fields = (
            'developer', 'name', 'status'
        )
        labels = {
            'developer': 'Desarrollador',
            'name': 'Nombre de Proyecto',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developer'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
        })


class TaskForm(ModelForm):
    type_task = forms.ModelChoiceField(queryset=TypeTask.objects.filter(status=True))

    class Meta:
        model = Task
        fields = (
            'type_task', 'task', 'state'
        )

        labels = {
            'type_task': 'Tipo Tarea',
            'task': 'Tarea',
            'state': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_task'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['task'].widget.attrs.update({
            'class': 'form-control',
        })


ProjectFormSet = inlineformset_factory(
    Project, Task, form=TaskForm,
    fields=['type_task', 'task', 'state'], extra=1, can_delete=True,
)
