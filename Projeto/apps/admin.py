from django.contrib import admin
from .models import Evento, Perfil, GrupoEstudo, FAQ, Voluntariado, Monitoria, IniciacaoCientifica, IniciativaEstudantil, Favorito

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'inicio_evento', 'fim_evento', 'tipo', 'vagas')
    list_filter = ('tipo', 'inicio_evento', 'fim_evento')
    search_fields = ('titulo', 'local', 'palestrante')
    ordering = ('-inicio_evento',)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(GrupoEstudo)
class GrupoEstudoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'numero_integrantes', 'professor_orientador', 'carga_horaria_semanal')
    search_fields = ('titulo', 'tema', 'professor_orientador')
    ordering = ('titulo',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'resposta', 'criado_em')
    search_fields = ('pergunta',)
    ordering = ('-criado_em',)

@admin.register(Voluntariado)
class VoluntariadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local_trabalho', 'organizacao_parceira', 'habilidades_requeridas', 'inicio_evento', 'fim_evento')  # Campos do Voluntariado
    search_fields = ('titulo', 'local_trabalho', 'organizacao_parceira')
    ordering = ('titulo',)

@admin.register(Monitoria)
class MonitoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'professor_orientador', 'disciplina', 'cadeiras_requeridas', 'requisitos', 'inicio_evento', 'fim_evento')  # Campos da Monitoria
    search_fields = ('titulo', 'professor_orientador', 'disciplina')
    ordering = ('titulo',)

@admin.register(IniciacaoCientifica)
class IniciacaoCientificaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'duracao', 'professor_orientador', 'bolsa_pesquisa', 'inicio_evento', 'fim_evento')  # Campos da Iniciação Científica
    search_fields = ('titulo', 'professor_orientador')
    ordering = ('titulo',)

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('user', 'objeto_favoritado', 'content_type', 'data_adicionado')  # Campos do Favorito
    search_fields = ('user',)
    ordering = ('data_adicionado',)

@admin.register(IniciativaEstudantil)
class IniciativaEstudantilAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'objetivo', 'docente_supervisor', 'site')  # Campos do IniciativaEstudantil
    search_fields = ('titulo', 'docente_supervisor')
    ordering = ('titulo',)

