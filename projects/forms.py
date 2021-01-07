from tasks.models import TypeTask
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tasks.forms import Task

from users.models import User

from .models import Project


class ProjectForm(ModelForm):
    developer = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='desarrolladores'),
        label='Desarrolladores',
    )

    class Meta:
        model = Project
        fields = (
            'developer', 'name'
        )
        labels = {
            'name': 'Nombre de Proyecto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developer'].widget.attrs.update({
            'data-role': 'select',
        })
        self.fields['name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-books'></span>",
        })


class TaskForm(ModelForm):
    type_task = forms.ModelChoiceField(
        queryset=TypeTask.objects.filter(status=True), label='Tipo Tarea')

    class Meta:
        model = Task
        fields = (
            'type_task', 'task', 'status'
        )

        labels = {
            'task': 'Tarea',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_task'].widget.attrs.update({
            'data-role': 'select',
            'class': 'form-control',
        })
        self.fields['task'].widget.attrs.update({
            'class': 'form-control',
        })


ProjectFormSet = inlineformset_factory(
    Project, Task, form=TaskForm,
    fields=['type_task', 'task', 'status'], extra=1, can_delete=True
)
