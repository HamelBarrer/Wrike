# Generated by Django 3.1.3 on 2020-11-27 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
