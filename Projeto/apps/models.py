from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        """Cria e retorna um usuário com email, nome e senha."""
        if not email:
            raise ValueError('O e-mail é obrigatório')
        if not nome:
            raise ValueError("O nome é obrigatório")
        
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        """Cria e retorna um superusuário com e-mail, nome e senha."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, nome, password, **extra_fields)

class Perfil(AbstractBaseUser):
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=128, null= True, blank= True)  # Gerenciado por AbstractBaseUser
    
    trocar_perfil = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Permissão para acessar o admin
    is_superuser = models.BooleanField(default=True)     

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome'] # 'email' é tratado por USERNAME_FIELD, e a senha é gerenciada por AbstractBaseUser

    objects = CustomUserManager()

    def __str__(self):
        return self.nome
    
    def has_perm(self, perm, obj=None):
        """Retorna True se o usuário tem a permissão especificada."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Retorna True se o usuário tem permissão para acessar o módulo específico."""
        return self.is_superuser

class Oportunidade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status_inscricoes = models.CharField(
        max_length=10,
        choices=[('abertas', 'Abertas'), ('em_breve', 'Abrem em breve'), ('fechadas', 'Fechadas')],
        default='fechadas'
    )
    tags = models.JSONField(blank=True, default=list)

    class Meta:
        abstract = True  # Define que esta classe é abstrata e não será criada no banco de dados

class Evento(Oportunidade):
    local = models.CharField(max_length=200)
    inicio_evento = models.DateField(default=timezone.now)
    fim_evento = models.DateField(null=True, blank=True)
    horario_de_inicio = models.TimeField(default=timezone.now)
    horario_de_termino = models.TimeField(default=timezone.now)
    palestrante = models.CharField(max_length=100, blank=True)
    opcao_palestrante = models.CharField(
        max_length=10,
        choices=[('nome', 'Informar nome'), ('indefinido', 'Indefinido / não informar')],
        default='indefinido'
    )
    participantes = models.JSONField(blank=True, default=list)
    vagas = models.IntegerField()
    tipo = models.CharField(
        max_length=10,
        choices=[('online', 'Online'), ('presencial', 'Presencial')],
    )

    def cadastrar(self, dados):
        """Método para cadastrar evento com os dados fornecidos."""
        self.titulo = dados.get('titulo')
        self.descricao = dados.get('descricao')
        self.local = dados.get('local')
        self.inicio_evento = dados.get('inicio_evento')
        self.fim_evento = dados.get('fim_evento')
        self.horario_de_inicio = dados.get('horario_de_inicio')
        self.horario_de_termino = dados.get('horario_de_termino')
        self.palestrante = dados.get('palestrante')
        self.opcao_palestrante = dados.get('opcao_palestrante')
        self.vagas = dados.get('vagas')
        self.tipo = dados.get('tipo')
        
        # Validações e lógica extra podem ser adicionadas aqui, se necessário
        self.save()  # Salva o evento no banco de dados
        
    def __str__(self):
        return self.titulo

    def is_online(self):
        return self.tipo == 'online'

    def duracao_evento(self):
        from datetime import datetime, timedelta
        data_inicio = datetime.combine(self.inicio_evento, self.horario_de_inicio)
        data_fim = datetime.combine(self.fim_evento, self.horario_de_termino)
        return data_fim - data_inicio


class GrupoEstudo(Oportunidade):
    
    tema = models.CharField(max_length=100)
    numero_integrantes = models.IntegerField()
    professor_orientador = models.CharField(max_length=100, blank=True)
    carga_horaria_semanal = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    dias_reuniao = models.JSONField(blank=True, default=list)  # Armazena dias da semana em formato JSON
    hora_reuniao = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo
    
class ProgramaOficial(Oportunidade):
    inicio_evento = models.DateField(default=timezone.now)
    fim_evento = models.DateField(null=True, blank=True)
    carga_horaria = models.IntegerField()  # em horas
    link_inscricao = models.URLField()

    class Meta:
        abstract = True  # Define que esta classe é abstrata e não será criada no banco de dados

class Voluntariado(ProgramaOficial):
    local_trabalho = models.CharField(max_length=100)
    organizacao_parceira = models.CharField(max_length=100)
    habilidades_requeridas = models.JSONField(default=list, blank=True)

    def cadastrar(self, dados):
        self.local_trabalho = dados.get('local_trabalho')
        self.organizacao_parceira = dados.get('organizacao_parceira')
        self.habilidades_requeridas = dados.get('habilidades_requeridas', [])
        self.save()  # Salva o objeto preenchido

class Monitoria(ProgramaOficial):
    professor_orientador = models.CharField(max_length=100)
    disciplina = models.CharField(max_length=100)
    cadeiras_requeridas = models.JSONField(default=list, blank=True)
    requisitos = models.JSONField(default=list, blank=True)

    def cadastrar(self, dados):
        self.professor_orientador = dados.get('professor_orientador')
        self.disciplina = dados.get('disciplina')
        self.cadeiras_requeridas = dados.get('cadeiras_requeridas', [])
        self.requisitos = dados.get('requisitos', [])
        self.save()

class IniciacaoCientifica(ProgramaOficial):
    duracao = models.DurationField()
    professor_orientador = models.CharField(max_length=100)
    bolsa_pesquisa = models.BooleanField()

    def cadastrar(self, dados):
        self.duracao = dados.get('duracao')
        self.professor_orientador = dados.get('professor_orientador')
        self.bolsa_pesquisa = dados.get('bolsa_pesquisa', False)
        self.save()