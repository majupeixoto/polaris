from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, Evento, GrupoEstudo, ProgramaOficial, Voluntariado, Monitoria, IniciacaoCientifica
from .forms import GrupoEstudoForm, EventoForm, PerfilForm, ProgramaOficialForm, VoluntariadoForm, MonitoriaForm, IniciacaoCientificaForm
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
            grupo_estudo = form.save(commit=False)
            grupo_estudo.tags = form.cleaned_data.get('tags', [])  # Salva as tags como lista
            grupo_estudo.save()
            messages.success(request, 'Grupo de estudo cadastrado com sucesso!')
            return redirect('cadastro_grupo_estudo')
        else:
            messages.error(request, 'Erro ao salvar o grupo de estudo. Verifique os dados e tente novamente.')
    else:
        form = GrupoEstudoForm()
    
    return render(request, 'apps/cadastro_grupo_estudo.html', {'form': form})

@login_required
def cadastrar_evento(request):
    user = request.user
    try:
        usuario = Perfil.objects.get(email=user.email)
    except Perfil.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('login')

    # Verifica o perfil do usuário antes de permitir o cadastro do evento
    if usuario.trocar_perfil == 0:
        messages.warning(request, "Você precisa trocar de perfil para acessar esta página.")
        return redirect('login')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)  # Cria o evento sem salvar no banco ainda
            # Processa os campos 'participantes' e 'tags' antes de salvar
            evento.participantes = form.cleaned_data['participantes']
            evento.tags = form.cleaned_data['tags']
            evento.save()  # Salva o evento com os dados completos
            messages.success(request, "Evento cadastrado com sucesso!")
            return redirect('visualizar_evento', evento_id=evento.id)
        else:
            messages.error(request, "Erro ao cadastrar evento. Verifique os dados e tente novamente.")
    else:
        form = EventoForm()

    return render(request, 'apps/cadastrar_evento.html', {'form': form})

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

@login_required
def listar_grupos_estudo(request):
    grupos = GrupoEstudo.objects.all()  # Busca todos os grupos de estudo
    context = {
        'grupos': grupos,
    }
    return render(request, 'apps/listar_grupos_estudo.html', context)

@login_required
def visualizar_grupo(request, grupo_id):
    grupo = get_object_or_404(GrupoEstudo, id=grupo_id)
    return render(request, 'apps/visualizar_grupo.html', {'grupo': grupo})

@login_required
def cadastrar_programa_oficial(request):
    if request.method == 'POST':
        tipo_programa = request.POST.get('tipo_programa')

        # Inicializa o formulário correto com base no tipo de programa
        if tipo_programa == 'voluntariado':
            form_programa = VoluntariadoForm(request.POST)
        elif tipo_programa == 'monitoria':
            form_programa = MonitoriaForm(request.POST)
        elif tipo_programa == 'iniciacao_cientifica':
            form_programa = IniciacaoCientificaForm(request.POST)
        else:
            messages.error(request, "Tipo de programa inválido.")
            return redirect('cadastrar_programa')

        # Verifica se o formulário é válido e salva a instância específica
        if form_programa.is_valid():
            form_programa.save()
            messages.success(request, f"{tipo_programa.capitalize()} cadastrado com sucesso!")
            return redirect('listar_programas')
        else:
            messages.error(request, "Erro no cadastro. Verifique os dados e tente novamente.")
    else:
        # Inicializa todos os formulários em branco para a renderização inicial
        form_voluntariado = VoluntariadoForm()
        form_monitoria = MonitoriaForm()
        form_iniciacao = IniciacaoCientificaForm()

    return render(request, 'apps/cadastrar_programa_oficial.html', {
        'form_voluntariado': form_voluntariado,
        'form_monitoria': form_monitoria,
        'form_iniciacao': form_iniciacao,
    })

@login_required
def visualizar_programa(request, programa_id):
    # Obtenção do programa específico com base no ID
    programa = get_object_or_404(ProgramaOficial, id=programa_id)
    
    # Determina o tipo de programa
    if hasattr(programa, 'voluntariado'):
        tipo = 'voluntariado'
        programa_especifico = programa.voluntariado
    elif hasattr(programa, 'monitoria'):
        tipo = 'monitoria'
        programa_especifico = programa.monitoria
    elif hasattr(programa, 'iniciacaocientifica'):
        tipo = 'iniciacao_cientifica'
        programa_especifico = programa.iniciacaocientifica
    else:
        tipo = 'desconhecido'
        programa_especifico = None

    return render(request, 'apps/visualizar_programa.html', {
        'programa': programa,
        'programa_especifico': programa_especifico,
        'tipo': tipo
    })