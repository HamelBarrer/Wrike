# Generated by Django 3.1.3 on 2021-01-06 19:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='developer',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
