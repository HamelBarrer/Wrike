from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'role',
        )
        labels = {
            'role': 'Rol',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-user'></span>",
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-user'></span>",
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-mail'></span>",
            'class': 'form-control',
        })
        self.fields['username'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-user'></span>",
            'class': 'form-control',
        })
        self.fields['password1'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-lock'></span>",
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-lock'></span>",
            'class': 'form-control',
        })
        self.fields['role'].widget.attrs.update({
            'data-role': 'select',
        })


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-user'></span>",
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-user'></span>",
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-mail'></span>",
            'class': 'form-control',
        })
        self.fields['username'].widget.attrs.update({
            'data-role': 'input',
            'data-prepend': "<span class='mif-user'></span>",
            'class': 'form-control',
        })
