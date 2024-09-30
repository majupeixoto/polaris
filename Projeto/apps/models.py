from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# lembrando: SEMPRE que modificar ou acrescentar uma models a gnt tem q fazer os comandos:
# python manage.py makemigrations
# e em seguida:
# python manage.py migrate
# python manage.py runserver

class Perfil(models.Model):
    nome = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=11)

    trocar_perfil = models.BooleanField()  # Campo booleano para distinguir entre alunos e funcionários

    def __str__(self):
        return (self.nome, self.email)