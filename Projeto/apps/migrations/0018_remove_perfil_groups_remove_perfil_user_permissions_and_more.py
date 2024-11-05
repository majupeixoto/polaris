# Generated by Django 5.1.1 on 2024-11-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0017_alter_perfil_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='perfil',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
