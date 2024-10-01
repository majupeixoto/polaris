from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil, Evento, GrupoEstudo
from .forms import GrupoEstudoForm
from django.http import HttpResponse

# Create your views here.

def cadastro_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        password = request.POST.get('password')
        perfil_tipo = request.POST.get('trocar_perfil')

        # Verificação de erros simples
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username já existe!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado!')
        else:
            # Cria o usuário e o perfil
            user = User.objects.create_user(username=username, email=email, password=password)
            perfil = Perfil.objects.create(nome=nome, username=username, email=email, telefone=telefone, trocar_perfil=perfil_tipo == 'on')
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
    
    return render(request, 'apps/cadastro_usuario.html')

def cadastro_grupo_estudo(request):
    if request.method == 'POST':
        form = GrupoEstudoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo de estudos cadastrado com sucesso!')
            return redirect('listar_grupos_estudo')
    else:
        form = GrupoEstudoForm()

    return render(request, 'apps/cadastro_grupo_estudo.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        trocar_perfil = request.POST.get('trocar_perfil')

        if trocar_perfil == 'aluno':
            return redirect(...)

        elif trocar_perfil == 'funcionario':
            return redirect(...)

    return render(request, 'apps/login.html')

def logout_view(request):
    logout(request)
    if "usuario" in request.session:
        del request.session["usuario"]
    return redirect('login')

def cadastrar_evento(request):
    if request.method == "POST":
        tipo_evento = request.POST['tipo_evento']
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']
        inicio_evento = request.POST['inicio_evento']
        fim_evento = request.POST['fim_evento']
        vagas = request.POST['vagas']
        tipo = request.POST['tipo']
        carga_horaria = request.POST['carga_horaria']
        local = request.POST['local']
        
        # Criando o evento
        Evento.objects.create(
            tipo_evento=tipo_evento,
            titulo=titulo,
            descricao=descricao,
            inicio_evento=inicio_evento,
            fim_evento=fim_evento,
            vagas=vagas,
            tipo=tipo,
            carga_horaria=carga_horaria,
            local=local,
        )
        
        return HttpResponse("Evento cadastrado com sucesso!")
    
    return render(request, 'apps/cadastrar_evento.html')

def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'apps/visualizar_evento.html', {'evento': evento})
