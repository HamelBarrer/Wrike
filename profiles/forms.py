from django import forms
from django.forms import ModelForm

from .models import Profile


class ProfileForm(ModelForm):
    phone = forms.CharField(
        min_length=10,
        max_length=14,
        label='Telefono',
        widget=forms.NumberInput(),
    )
    class Meta:
        model = Profile
        fields = (
            'avatar', 'phone', 'direction',
        )
        labels = {
            'direction': 'Direccion',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({
            'data-role': 'file',
            'data-mode': 'drop',
        })
        self.fields['phone'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-phonelink-setup'></span>",
            'class': 'form-control',
        })
        self.fields['direction'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-map'></span>",
            'class': 'form-control',
        })
