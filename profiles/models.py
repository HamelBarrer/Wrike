from PIL import Image
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.png', upload_to='profiles/')
    phone = models.CharField(max_length=14, blank=True, null=True)
    direction = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now=timezone.now())

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def set_role_user(sender, instance, *args, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def set_avatar_user(sender, instance, *args, **kwargs):
    if instance.avatar:
        img = Image.open(instance.avatar.path)

        if img.width > 400 and img.height > 400:
            size = (400, 400)
            img.thumbnail(size)
            img.save(instance.avatar.path)
