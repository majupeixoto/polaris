# Generated by Django 5.1.1 on 2024-11-28 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0034_favorito"),
    ]

    operations = [
        migrations.CreateModel(
            name="FAQ",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pergunta", models.CharField(max_length=255)),
                ("resposta", models.TextField()),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
