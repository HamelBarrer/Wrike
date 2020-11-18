import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from projects.models import Project

from users.models import Developer


class TypeTask(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    slug = models.SlugField(max_length=60, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de Creacion')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo tarea'
        verbose_name_plural = 'Tipo tareas'


class Task(models.Model):
    developer = models.ManyToManyField(Developer, verbose_name='Desarrollador')
    type_task = models.ForeignKey(
        TypeTask, on_delete=models.CASCADE, verbose_name='Tipo Tarea')
    task = models.CharField(max_length=50, verbose_name='Tarea')
    description = models.TextField(verbose_name='Descripcion')
    state = models.BooleanField(default=True, verbose_name='Estado')
    slug = models.SlugField(max_length=60, unique=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Proyecto')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de Creacion')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Fecha de Actualizacion')

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'


class Activities(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    process = models.BooleanField(default=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'


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
