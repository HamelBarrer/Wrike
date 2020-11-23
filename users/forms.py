from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'avatar', 'email', 'username', 'password1', 'password2', 'role',
        )
        labels = {
            'role': 'Rol',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'id': 'icon_firstName',
        })
        self.fields['last_name'].widget.attrs.update({
            'id': 'icon_lastName',
        })
        self.fields['email'].widget.attrs.update({
            'id': 'icon_email',
        })
        self.fields['username'].widget.attrs.update({
            'id': 'icon_username',
        })
        self.fields['password1'].widget.attrs.update({
            'id': 'icon_password1',
        })
        self.fields['password2'].widget.attrs.update({
            'id': 'icon_password2',
        })
