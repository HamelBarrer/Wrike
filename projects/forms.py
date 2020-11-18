from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tasks.forms import Task

from .models import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = (
            'developer', 'name', 'visibility', 'status'
        )
        labels = {
            'developer': 'Desarrollador',
            'name': 'Nombre de Proyecto',
            'visibility': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developer'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['visibility'].widget.attrs.update({
            'class': 'form-check-input',
        })


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = (
            'type_task', 'task',
        )


ProjectFormSet = inlineformset_factory(
    Project, Task, form=TaskForm,
    fields=['type_task', 'task'], extra=1, can_delete=True,
)
