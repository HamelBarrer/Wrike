from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from tasks.forms import Task

from .models import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = (
            'developer', 'name',
        )
        labels = {
            'developer': 'Desarrollador',
            'name': 'Nombre de Proyecto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'id': 'icon_name',
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
