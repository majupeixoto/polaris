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
    opcoes = [
        ('design', 'Design'),
        ('ciencias da computacao', 'Ciências da Computação'),
        ('sistemas de informacao', 'Sistemas de Informação'),
        ('analise e desenvolvimento de sistemas', 'Análise e Desenvolvimento de Sistemas'),
        ('gestao de tecnologia da informacao', 'Gestão de Tecnologia da Informação')
    ]
    curso = models.CharField(max_length=50, choices=opcoes, null=True)
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

    OPCOES_PALESTRANTE = [
        ('nome', 'Informar nome'),
        ('indefinido', 'Indefinido / não informar'),
    ]

    titulo = models.CharField(max_length=100)
    local = models.CharField(max_length=200)
    descricao = models.TextField()
    inicio_evento = models.DateField(default=timezone.now)
    fim_evento = models.DateField(default=timezone.now)
    horario_de_inicio = models.TimeField(default=timezone.now)
    horario_de_termino = models.TimeField(default=timezone.now)
    palestrante = models.CharField(max_length=100, blank=True)  # Pode ser vazio
    opcao_palestrante = models.CharField(max_length=10, choices=OPCOES_PALESTRANTE, default='indefinido')  # Adicionado para armazenar a opção escolhida
    participantes = models.CharField(max_length=100, blank=True)  # Pode ser vazio
    vagas = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)  # Escolha entre 'Online' e 'Presencial'

    def __str__(self):
        return self.titulo

    def is_online(self):
        return self.tipo == 'online'

    def duracao_evento(self):
        from datetime import datetime, timedelta
        data_inicio = datetime.combine(self.inicio_evento, self.horario_de_inicio)
        data_fim = datetime.combine(self.fim_evento, self.horario_de_termino)
        return data_fim - data_inicio


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