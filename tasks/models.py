import uuid

from django.db import models
from django.db.models.aggregates import Count
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save

from projects.models import Project


class TypeTask(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type_task = models.ForeignKey(TypeTask, on_delete=models.CASCADE)
    task = models.CharField(max_length=50)
    description = models.TextField()
    status = models.BooleanField(default=False)
    percentage = models.IntegerField(default=0)
    slug = models.SlugField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now())
    updated_at = models.DateTimeField(auto_now=timezone.now())

    def __str__(self):
        return self.task


class Activities(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.name


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


@receiver(pre_save, sender=Task)
def set_completed_project(sender, instance, **kwargs):
    total = Task.objects.filter(project=instance.project, status=True).count()
    print(total)
