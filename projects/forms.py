from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tasks.forms import Task

from .models import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = (
            'developer', 'name', 'status'
        )
        labels = {
            'developer': 'Desarrolladore',
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
    class Meta:
        model = Task
        fields = (
            'type_task', 'task', 'state'
        )

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
