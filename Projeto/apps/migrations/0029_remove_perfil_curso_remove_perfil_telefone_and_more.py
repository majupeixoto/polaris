# Generated by Django 5.1.1 on 2024-11-28 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0028_alter_grupoestudo_carga_horaria_semanal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='telefone',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='trocar_perfil',
        ),
    ]
