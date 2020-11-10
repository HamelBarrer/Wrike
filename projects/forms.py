from django.forms import ModelForm

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = (
            'name', 'state',
        )
        fields = {
            'name': 'Nombre de Proyecto',
            'state': 'Estado',
        }
