from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, Evento, GrupoEstudo
from .forms import GrupoEstudoForm, EventoForm, PerfilForm  # Adicione o PerfilForm aqui
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Autentica usando o email
        user = authenticate(request, email=email, password=senha)  # Usando 'email' aqui

        if user is not None:
            login(request, user)

            if user.trocar_perfil == 1: 
                return redirect('home_funcionario')  # funcionário
            else:
                return redirect('home_aluno')  # aluno
        else:
            messages.error(request, "Credenciais inválidas. Por favor, tente novamente.")
    
    return render(request, 'apps/login.html')

def logout_view(request):
    logout(request)
    if "usuario" in request.session:
        del request.session["usuario"]
    return redirect('login')

def cadastro_usuario(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo perfil no banco de dados
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
    else:
        form = PerfilForm()

    return render(request, 'apps/cadastro_usuario.html', {'form': form})




@login_required
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

@login_required
def cadastrar_evento(request):
    user = request.user
    try:
        usuario = Perfil.objects.get(email=user.email)  # Acesse o email como usuário
    except Perfil.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('login')  # Redireciona para o login se o perfil não existir

    # Verifique se o usuário precisa trocar de perfil
    if usuario.trocar_perfil == 0:
        messages.warning(request, "Você precisa trocar de perfil para acessar esta página.")
        return redirect('login')  # Redireciona se o perfil não for o correto

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()  # Salva o evento e armazena na variável
            messages.success(request, "Evento cadastrado com sucesso!")  # Mensagem de sucesso
            return redirect('visualizar_evento', evento_id=evento.id)  # Redireciona passando o ID do evento
        else:
            messages.error(request, "Erro ao cadastrar evento. Verifique os dados e tente novamente.")
    else:
        form = EventoForm()  # Cria um novo formulário

    return render(request, 'apps/cadastrar_evento.html', {'form': form})  # Passa o formulário para o template

@login_required
def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'apps/visualizar_evento.html', {'evento': evento})




@login_required
def home_aluno(request):
    user = request.user
    usuario = Perfil.objects.get(email=user.email)
    if user.trocar_perfil == 1:
        return redirect(login)
    else:
        if request.user.is_anonymous:
            return redirect(login)
        else:
            eventos = Evento.objects.all()
            return render(request, 'apps/home_aluno.html', {'eventos': eventos})

@login_required
def home_funcionario(request):
    user = request.user
    usuario = Perfil.objects.get(email=user.email)
    if user.trocar_perfil == 0:
        return redirect(login)
    else:
        if request.user.is_anonymous:
            return redirect(login)
        else:
            eventos = Evento.objects.all()
            return render(request, 'apps/home_funcionario.html', {'eventos': eventos})


@login_required
def listar_eventos(request):
    user = request.user
    try:
        usuario = Perfil.objects.get(email=user.email)
    except Perfil.DoesNotExist:
        messages.error(request, "Perfil não encontrado.")
        return redirect('login')

    # Verifica se o usuário é um funcionário
    if usuario.funcionario == 1:
        return redirect('login')

    # Obtém todos os eventos
    eventos = Evento.objects.all()
    context = {
        'eventos': eventos,
    }

    return render(request, 'apps/listar_eventos.html', context)
