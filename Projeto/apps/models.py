from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Cria e retorna um usuário com email e senha."""
        if not email:
            raise ValueError('O e-mail deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria e retorna um superusuário com e-mail e senha."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Perfil(AbstractBaseUser):
    opcoes = [
        ('design', 'Design'),
        ('ciencias da computacao', 'Ciências da Computação'),
        ('sistemas de informacao', 'Sistemas de Informação'),
        ('analise e desenvolvimento de sistemas', 'Análise e Desenvolvimento de Sistemas'),
        ('gestao de tecnologia da informacao', 'Gestão de Tecnologia da Informação'),
    ]

    curso = models.CharField(max_length=50, choices=opcoes, null=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=128, null= True, blank= True)  # Senha em texto puro

    telefone = models.CharField(max_length=11)  # Considere usar django-phonenumber-field para validação
    trocar_perfil = models.BooleanField(default=False)  # Distinção entre aluno e funcionário
    is_staff = models.BooleanField(default=False)         
    is_superuser = models.BooleanField(default=True)     

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'telefone']  # Campos obrigatórios para criação do usuário

    objects = CustomUserManager()

    def __str__(self):
        return self.nome
    
    def has_perm(self, perm, obj=None):
        """Retorna True se o usuário tem a permissão especificada."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Retorna True se o usuário tem permissão para acessar o módulo específico."""
        return self.is_superuser

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