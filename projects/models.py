from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from users.models import Developer

from tasks.models import Task


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    developer = models.ManyToManyField(Developer)
    state = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Project)
def set_project_slug(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
