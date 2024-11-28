from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    IniciativaEstudantilListView,
    IniciativaEstudantilDetailView,
    IniciativaEstudantilCreateView,
    IniciativaEstudantilUpdateView,
    IniciativaEstudantilDeleteView,
    FavoritoListView,
    faq_view
)

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro_grupo_estudo/', views.cadastro_grupo_estudo, name='cadastro_grupo_estudo'), 
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('evento/<int:evento_id>/', views.visualizar_evento, name='visualizar_evento'),
    path('home_aluno/', views.home_aluno, name = 'home_aluno'),
    path('home_funcionario/', views.home_funcionario, name = 'home_funcionario'),
    path('listar_eventos/', views.listar_eventos, name='listar_eventos'),
    path('listar_grupos_estudo/', views.listar_grupos_estudo, name='listar_grupos_estudo'),
    path('grupos/<int:grupo_id>/', views.visualizar_grupo, name='visualizar_grupo'),
    path('programa/<str:tipo>/<int:id>/', views.visualizar_programa, name='detalhes_programa'),
    path('selecionar_programa/', views.selecionar_tipo_programa, name='selecionar_programa'),
    path('cadastrar_voluntariado/', views.cadastrar_voluntariado, name='cadastrar_voluntariado'),
    path('cadastrar_monitoria/', views.cadastrar_monitoria, name='cadastrar_monitoria'),
    path('cadastrar_iniciacao_cientifica/', views.cadastrar_iniciacao_cientifica, name='cadastrar_iniciacao_cientifica'),
    path('iniciativas/', IniciativaEstudantilListView.as_view(), name='iniciativa_list'),
    path('iniciativas/<int:pk>/', IniciativaEstudantilDetailView.as_view(), name='iniciativa_detail'),
    path('iniciativas/criar/', IniciativaEstudantilCreateView.as_view(), name='iniciativa_create'),
    path('iniciativas/<int:pk>/editar/', IniciativaEstudantilUpdateView.as_view(), name='iniciativa_update'),
    path('iniciativas/<int:pk>/excluir/', IniciativaEstudantilDeleteView.as_view(), name='iniciativa_delete'),
    path('favoritos/', FavoritoListView.as_view(), name='favoritos'),
    path('favoritar_evento/', views.favoritar_evento, name='favoritar_evento'),
    path('faq/', faq_view, name='faq'),
    path('evento/<int:evento_id>/alterar/', views.alterar_evento, name='alterar_evento'),
    path('evento/<int:evento_id>/excluir/', views.excluir_evento, name='excluir_evento'),
]