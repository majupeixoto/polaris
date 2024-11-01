from django.contrib import admin
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'trocar_perfil')
    search_fields = ('email', 'nome')

admin.site.register(Perfil, PerfilAdmin)