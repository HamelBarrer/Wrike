from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from users.models import Developer


class Project(models.Model):
    STATUS_CHOICES = (
        ('approver', 'Aprovado'),
        ('process', 'En Proceso'),
        ('inactive', 'Inactivo'),
    )

    name = models.CharField(max_length=50, unique=True)
    developer = models.ManyToManyField(Developer)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[1])
    slug = models.SlugField(max_length=50, unique=True)
    porcentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Project)
def set_project_slug(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
