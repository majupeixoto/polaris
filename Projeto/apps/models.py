from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        """Cria e retorna um usuário com email, nome e senha."""
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        if not nome:
            raise ValueError("O nome é obrigatório.")

        email = self.normalize_email(email)

        # Configura valores padrão para novos usuários
        extra_fields.setdefault('is_staff', False)  # Alunos não são staff
        extra_fields.setdefault('is_superuser', False)  # Alunos não são superusuários

        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user


    def create_superuser(self, email, nome, password=None, **extra_fields):
        """Cria e retorna um superusuário com email, nome e senha."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuários precisam ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuários precisam ter is_superuser=True.')

        return self.create_user(email, nome, password, **extra_fields)

class Perfil(AbstractBaseUser):
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=128, null= True, blank= True)  # Gerenciado por AbstractBaseUser

    is_staff = models.BooleanField(default=False)  # Permissão para acessar o admin
    is_superuser = models.BooleanField(default=False)     

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
    STATUS_CHOICES = [
        ('abertas', 'Abertas'),
        ('em_breve', 'Abrem em breve'),
        ('fechadas', 'Fechadas'),
    ]
    
    titulo = models.CharField(max_length=255, default="")
    descricao = models.TextField(default="")
    status_inscricoes = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='fechadas'
    )
    tags = models.JSONField(blank=True, default=list)

    class Meta:
        abstract = True  # classe abstrata

    def excluir_oportunidade(self):
        """Método para excluir a oportunidade."""
        self.delete()

    def fechar_inscricoes(self):
        """Fecha as inscrições."""
        self.status_inscricoes = 'fechadas'
        self.save()

    def abrir_inscricoes(self):
        """Abre as inscrições."""
        self.status_inscricoes = 'abertas'
        self.save()

    def inscrever_estudante(self, estudante):
        """Método para inscrever um estudante na oportunidade."""
        # A lógica de inscrição depende do seu modelo de dados, mas pode ser implementada aqui
        pass

    def publicar_oportunidade(self):
        """Publica a oportunidade."""
        self.status_inscricoes = 'abertas'  # Exemplo
        self.save()

    def filtrar_oportunidade(self, **kwargs):
        """Filtra oportunidades com base em parâmetros fornecidos."""
        oportunidades = Oportunidade.objects.filter(**kwargs)
        return oportunidades

    def editar_oportunidade(self, titulo=None, descricao=None, status_inscricoes=None, tags=None):
        """Método para editar os campos da oportunidade."""
        if titulo:
            self.titulo = titulo
        if descricao:
            self.descricao = descricao
        if status_inscricoes:
            self.status_inscricoes = status_inscricoes
        if tags is not None:
            self.tags = tags
        self.save()

class Evento(Oportunidade):
    local = models.CharField(max_length=200)
    inicio_evento = models.DateField(default=timezone.now)
    fim_evento = models.DateField(default=timezone.now, null=True, blank=True)
    horario_de_inicio = models.TimeField(default=timezone.now)
    horario_de_termino = models.TimeField(default=timezone.now)
    palestrante = models.CharField(max_length=100, blank=True)
    opcao_palestrante = models.CharField(
        max_length=10,
        choices=[('nome', 'Informar nome'), ('indefinido', 'Indefinido / não informar')],
        default='indefinido'
    )
    #participantes = models.JSONField(blank=True, default=list)
    participantes = models.ManyToManyField('Perfil', related_name='eventos', blank=True)
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
    inicio_evento = models.DateTimeField(default=timezone.now)
    fim_evento = models.DateTimeField(default=timezone.now)
    carga_horaria = models.IntegerField(default=0)
    tema = models.CharField(max_length=255, blank=True, null=True)
    periodicidade = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=255, blank=True, null=True)
    links = models.URLField(max_length=500, blank=True, null=True)
    link_inscricao = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        abstract = True
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

class IniciativaEstudantil(Oportunidade):
    objetivo = models.TextField(max_length=255, default="Sem objetivo definido")
    docente_supervisor = models.CharField(max_length=255)
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo
    

class Favorito(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    # Campos para GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    objeto_favoritado = GenericForeignKey('content_type', 'object_id')
    
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')  # Evita duplicidade de favoritos
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f'Favorito: {self.user} - {self.objeto_favoritado}'

class FAQ(models.Model):
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pergunta

