from datetime import date

from django.db.models import F
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save

from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    developer = models.ManyToManyField(User)
    status = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, unique=True)
    percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    update_at = models.DateTimeField(auto_now=timezone.now())

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Project)
def set_project_slug(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
