from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'password1', 'password2', 'first_name', 'last_name'
        )
