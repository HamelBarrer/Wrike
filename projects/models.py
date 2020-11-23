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

    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    developer = models.ManyToManyField(Developer, verbose_name='Desarrollador')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[1])
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de Creacion')
    update_at = models.DateTimeField(
        auto_now=True, verbose_name='Fecha de Actualizacion')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'


@receiver(pre_save, sender=Project)
def set_project_slug(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
