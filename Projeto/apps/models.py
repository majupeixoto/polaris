from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
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
    email = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    telefone = models.CharField(max_length=11)  # Para padronizar, pode-se usar django-phonenumber-field
    trocar_perfil = models.BooleanField(default=False)  # Distinção entre aluno e funcionário

    def __str__(self):
        return self.nome
    
class Evento(models.Model):
    TIPO_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)  # Escolha entre 'Online' e 'Presencial'
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    inicio_evento = models.DateTimeField()
    fim_evento = models.DateTimeField()
    vagas = models.IntegerField()
    carga_horaria = models.DecimalField(max_digits=5, decimal_places=2)  # Ex: 2.5 para 2 horas e 30 minutos
    local = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo

    # Método para formatar carga horária como horas e minutos
    def carga_horaria_formatada(self):
        horas = int(self.carga_horaria)
        minutos = int((self.carga_horaria - horas) * 60)
        return f"{horas:02d} hora(s) e {minutos:02d} minuto(s)"
    
    # Método para verificar se o evento é online
    def is_online(self):
        return self.tipo == 'online'

    # Método para verificar a duração total do evento
    def duracao_evento(self):
        return self.fim_evento - self.inicio_evento


class GrupoEstudo(models.Model):
    titulo = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    numero_integrantes = models.IntegerField()
    descricao = models.TextField()
    professor_orientador = models.CharField(max_length=100)
    carga_horaria_semanal = models.DecimalField(max_digits=4, decimal_places=2)
    dias_reuniao = models.CharField(max_length=100)  # Ex: "Segunda, Quarta"
    hora_reuniao = models.TimeField()

    def __str__(self):
        return self.titulo