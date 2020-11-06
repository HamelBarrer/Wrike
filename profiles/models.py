from PIL import Image
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from users.models import (
    Administrator,
    Developer,
)


class ProfileAdministrator(models.Model):
    user = models.OneToOneField(Administrator, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class ProfileDeveloper(models.Model):
    user = models.OneToOneField(Developer, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


@receiver(post_save, sender=Administrator)
def set_profile_administrator(sender, instance, *args, **kwargs):
    if kwargs.get('created', False):
        ProfileAdministrator.objects.create(user=instance)


@receiver(post_save, sender=Developer)
def set_profile_developer(sender, instance, *args, **kwargs):
    if kwargs.get('created', False):
        ProfileDeveloper.objects.create(user=instance)


@receiver(pre_save, sender=ProfileAdministrator)
def set_slug_profile_administrator(sender, instance, *args, **kwargs):
    if instance.user:
        instance.slug = slugify(instance.user)


@receiver(pre_save, sender=ProfileDeveloper)
def set_slug_profile_developer(sender, instance, *args, **kwargs):
    if instance.user:
        instance.slug = slugify(instance.user)
