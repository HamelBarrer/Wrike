from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


class User(AbstractUser):

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
