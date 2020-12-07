from django import forms
from django.forms import ModelForm

from .models import Profile


class ProfileForm(ModelForm):
    phone = forms.NumberInput()
    class Meta:
        model = Profile
        fields = (
            'avatar', 'phone', 'direction',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['direction'].widget.attrs.update({
            'class': 'form-control'
        })
