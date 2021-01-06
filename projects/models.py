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
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50, unique=True)
    percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    update_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Project)
def set_project_slug(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(user_logged_in, sender=User)
def set_update_date(sender, request, user, **kwargs):
    projects = Project.objects.all()
    for project in projects:
        hoy = date.today()
        if hoy >= project.end_date:
            project.status = False
        else:
            project.status = True
