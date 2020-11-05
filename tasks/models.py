import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from users.models import User


class TypeTask(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_task = models.ForeignKey(TypeTask, on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    description = models.TextField()
    state = models.BooleanField(default=True)
    slug = models.SlugField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


@receiver(pre_save, sender=TypeTask)
def set_slug_typetasks(sender, instance, *args, **kwargs):
    if instance.name:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Task)
def set_slug_task(sender, instance, *args, **kwargs):
    if instance.task and not instance.slug:
        slug = slugify(instance.task)
        while Task.objects.filter(slug=slug).exists():
            slug = slugify(
                f'{instance.task}-{str(uuid.uuid4())[:8]}'
            )

        instance.slug = slug
