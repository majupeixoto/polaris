from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('cadastro_grupo_estudo/', views.cadastro_grupo_estudo, name='cadastro_grupo_estudo'), 
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('evento/<int:evento_id>/', views.visualizar_evento, name='visualizar_evento'),
]