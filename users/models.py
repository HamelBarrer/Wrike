from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed


class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrador', 'Administrador'),
        ('desarrollador', 'Desarrollador'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


@receiver(post_save, sender=User)
def set_role_user(sender, instance, *args, **kwargs):
    if instance.role:
        if instance.role == 'administrador':
            group = Group.objects.get(name='administradores')
            instance.groups.update(group)
        else:
            group = Group.objects.get(name='desarrolladores')
            instance.groups.update(group)
