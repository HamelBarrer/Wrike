from django import forms
from django.forms import ModelForm

from users.models import Developer, User

from .models import Project


class ProjectForm(ModelForm):
    
    class Meta:
        model = Project
        fields = (
            'developer', 'name', 'visibility',
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
