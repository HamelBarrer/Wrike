# Generated by Django 3.1.3 on 2020-11-18 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
            ],
            options={
                'verbose_name': 'Perfil Administrador',
                'verbose_name_plural': 'Perfil de Administradores',
            },
        ),
        migrations.CreateModel(
            name='ProfileDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
            ],
            options={
                'verbose_name': 'Perfil Desarrollador',
                'verbose_name_plural': 'Perfil de Desarrolladores',
            },
        ),
    ]
