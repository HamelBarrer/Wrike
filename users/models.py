from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrador', 'Administrador'),
        ('desarrollador', 'Desarrollador'),
    )

    avatar = models.ImageField(default='avatar.png', upload_to='users/')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def set_role_user(sender, instance, *args, **kwargs):
    if kwargs.get('created', False):
        if instance.role == 'administrador':
            Administrator.objects.create(user=instance)
            group = Group.objects.get(name='administradores')
            instance.groups.add(group)
        else:
            Developer.objects.create(user=instance)
            group = Group.objects.get(name='desarrolladores')
            instance.groups.add(group)


@receiver(post_save, sender=User)
def set_avatar_user(sender, instance, *args, **kwargs):
    if instance.avatar:
        img = Image.open(instance.avatar.path)

        if img.width > 400 and img.height > 400:
            size = (400, 400)
            img.thumbnail(size)
            img.save(instance.avatar.path)
