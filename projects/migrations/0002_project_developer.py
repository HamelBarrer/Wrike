# Generated by Django 3.0 on 2021-01-08 20:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='developer',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
