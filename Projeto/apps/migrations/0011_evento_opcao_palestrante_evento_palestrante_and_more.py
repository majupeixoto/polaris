# Generated by Django 5.1.1 on 2024-10-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_remove_evento_opcaonome'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='opcao_palestrante',
            field=models.CharField(choices=[('nome', 'Informar nome'), ('indefinido', 'Indefinido / não informar')], default='indefinido', max_length=10),
        ),
        migrations.AddField(
            model_name='evento',
            name='palestrante',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='evento',
            name='participantes',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]