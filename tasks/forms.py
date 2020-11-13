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
    developers = Project.objects.values_list('developer__user', flat=True)
    developer = forms.ModelChoiceField(Task.objects.filter(developer__in=developers))

    class Meta:
        model = Task
        fields = (
            'developer', 'description', 'type_task', 'task','state', 'project', 'slug'
        )


class ActivitiesForm(ModelForm):
    class Meta:
        model = Activities
        fields = (
            'name', 'process',
        )


TaskFormSet = inlineformset_factory(
    Task, Activities, form=ActivitiesForm,
    fields=['name', 'process'], extra=1, can_delete=True
)
