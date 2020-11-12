from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrador', 'Administrador'),
        ('desarrollador', 'Desarrollador'),
    )

    avatar = models.ImageField(default='avatar.png', upload_to='users/')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name='Rol')


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creted_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')

    def __str__(self):
        return self.user.username


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def set_role_user(sender, instance, *args, **kwargs):
    if kwargs.get('created', False):
        if instance.role == 'administrador':
            Administrator.objects.create(user=instance)
        else:
            Developer.objects.create(user=instance)


@receiver(post_save, sender=User)
def set_avatar_user(sender, instance, *args, **kwargs):
    if instance.avatar:
        img = Image.open(instance.avatar.path)

        if img.width > 400 and img.height > 400:
            size = (400, 400)
            img.thumbnail(size)
            img.save(instance.avatar.path)
