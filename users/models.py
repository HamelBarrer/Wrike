from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrador', 'Administrador'),
        ('desarrollador', 'Desarrollador'),
    )

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
        else:
            Developer.objects.create(user=instance)
