from django.forms import ModelForm
from django.forms.models import inlineformset_factory


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
            'name': 'Tipo tarea',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-bookmark'></span>",
            'class': 'form-control',
        })


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = (
            'description',
        )
        labels = {
            'description': 'Descripcion',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({
            'data-role': 'textarea',
            'data-prepend': "<span class='mif-description'></span>",
        })


class ActivitiesForm(ModelForm):
    class Meta:
        model = Activities
        fields = (
            'name', 'process',
        )
        labels = {
            'name': 'Nombre',
            'process': 'Proseso',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-bookmark'></span>",
            'class': 'form-control',
        })
        self.fields['process'].widget.attrs.update({
            'data-role': 'checkbox'
        })


TaskFormSet = inlineformset_factory(
    Task, Activities, form=ActivitiesForm,
    fields=['name', 'process'], extra=1, can_delete=True
)
