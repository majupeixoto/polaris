from django.contrib import admin
from .models import Evento, Perfil, GrupoEstudo

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'inicio_evento', 'fim_evento', 'tipo', 'vagas')
    list_filter = ('tipo', 'inicio_evento', 'fim_evento')
    search_fields = ('titulo', 'local', 'palestrante')
    ordering = ('-inicio_evento',)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'curso', 'trocar_perfil', 'is_staff', 'is_superuser')
    list_filter = ('curso', 'trocar_perfil', 'is_staff', 'is_superuser')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(GrupoEstudo)
class GrupoEstudoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'numero_integrantes', 'professor_orientador', 'carga_horaria_semanal')
    search_fields = ('titulo', 'tema', 'professor_orientador')
    ordering = ('titulo',)