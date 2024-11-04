from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro_grupo_estudo/', views.cadastro_grupo_estudo, name='cadastro_grupo_estudo'), 
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('evento/<int:evento_id>/', views.visualizar_evento, name='visualizar_evento'),
    path('home_aluno/', views.home_aluno, name = 'home_aluno'),
    path('home_funcionario/', views.home_funcionario, name = 'home_funcionario'),
    path('logout/', views.logout_view, name='logout'),
    path('listar_eventos/', views.listar_eventos, name='listar_eventos'),
    path('listar_grupos_estudo/', views.listar_grupos_estudo, name='listar_grupos_estudo'),
    path('grupos/<int:grupo_id>/', views.visualizar_grupo, name='visualizar_grupo'),
]