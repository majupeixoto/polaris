from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    path('cadastrar_evento/', views.cadastrar_evento, name='cadastrar_evento'),
    path('evento/<int:evento_id>/', views.visualizar_evento, name='visualizar_evento'),
]