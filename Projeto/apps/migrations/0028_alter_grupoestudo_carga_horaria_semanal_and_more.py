# Generated by Django 5.1.1 on 2024-11-07 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0027_alter_grupoestudo_dias_reuniao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoestudo',
            name='carga_horaria_semanal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='grupoestudo',
            name='dias_reuniao',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='grupoestudo',
            name='hora_reuniao',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grupoestudo',
            name='professor_orientador',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
