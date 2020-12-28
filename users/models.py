from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


class User(AbstractUser):

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


@receiver(post_save, sender=User)
def group_user(sender, instance, *args, **kwargs):
    if instance.groups:
        print(instance.groups)
        if instance.groups == 'administradores':
            group = Group.objects.get(name='administradores')
            instance.groups.clear()
            instance.groups.add(group)
        else:
            group = Group.objects.get(name='desarrolladores')
            instance.groups.clear()
            instance.groups.add(group)
