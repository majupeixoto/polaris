from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, Evento, GrupoEstudo, ProgramaOficial, Voluntariado, Monitoria, IniciacaoCientifica, IniciativaEstudantil, Favorito
from .forms import GrupoEstudoForm, EventoForm, PerfilForm, VoluntariadoForm, MonitoriaForm, IniciacaoCientificaForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Autentica o usuário usando o email
        user = authenticate(request, email=email, password=senha)  # Usando 'email' aqui

        if user is not None:
            login(request, user)

            # Verifica se o usuário é um superusuário (funcionário)
            if user.is_superuser:  # funcionário
                return redirect('home_funcionario')
            else:  # aluno
                return redirect('home_aluno')
        else:
            messages.error(request, "Credenciais inválidas. Por favor, tente novamente.")
    
    return render(request, 'apps/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para a página de login após o logout


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
            # Obtém as tags do campo escondido e as converte de JSON para uma lista
            grupo_estudo.tags = form.cleaned_data.get('tags', [])
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

    # Verifica se o usuário é superusuário antes de permitir o cadastro do evento
    if not user.is_superuser:  # Se não for superusuário, redireciona
        messages.warning(request, "Você precisa ser um superusuário para acessar esta página.")
        return redirect('login')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)  # Cria o evento sem salvar no banco ainda
            # Processa os campos 'participantes' e 'tags' antes de salvar
            evento.participantes.set(form.cleaned_data['participantes'])  # Caso seja ManyToManyField
            evento.tags.set(form.cleaned_data['tags'])  # Caso seja ManyToManyField
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
    
    # Verifica se o usuário é um superusuário (funcionário)
    if user.is_superuser:
        return redirect('home_funcionario')  # Redireciona para a página de funcionário se for superusuário
    
    # Verifica se o usuário é anônimo (não autenticado)
    if request.user.is_anonymous:
        return redirect('login')  # Redireciona para o login se o usuário não estiver autenticado
    
    # Se for um aluno e o usuário estiver autenticado, carrega os eventos
    eventos = Evento.objects.all()
    return render(request, 'apps/home_aluno.html', {'eventos': eventos})


@login_required
def home_funcionario(request):
    user = request.user
    
    # Verifica se o usuário é um superusuário (funcionário)
    if not user.is_superuser:
        return redirect('login')  # Redireciona para login se não for funcionário

    # Se o usuário não for anônimo, carrega os eventos
    if request.user.is_authenticated:
        eventos = Evento.objects.all()
        return render(request, 'apps/home_funcionario.html', {'eventos': eventos})
    else:
        return redirect('login')  # Se o usuário não estiver autenticado, redireciona para login



@login_required
def listar_eventos(request):
    user = request.user
    try:
        usuario = Perfil.objects.get(email=user.email)
    except Perfil.DoesNotExist:
        messages.error(request, "Perfil não encontrado.")
        return redirect('login')

    # Verifica se o usuário NÃO é um superusuário (ou seja, é um aluno)
    if usuario.is_superuser:
        messages.warning(request, "Funcionários não têm acesso a esta página.")
        return redirect('home_funcionario')  # Redireciona para a home do funcionário

    # Obtém todos os eventos para o aluno
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

def selecionar_tipo_programa(request):
    return render(request, 'apps/selecionar_tipo_programa.html')

def cadastrar_voluntariado(request):
    if request.method == 'POST':
        form = VoluntariadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voluntariado cadastrado com sucesso!')
            return redirect('listar_programas')
    else:
        form = VoluntariadoForm()
    return render(request, 'apps/cadastrar_voluntariado.html', {'form': form})

def cadastrar_monitoria(request):
    if request.method == 'POST':
        form = MonitoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Monitoria cadastrada com sucesso!')
            return redirect('listar_programas')
    else:
        form = MonitoriaForm()
    return render(request, 'apps/cadastrar_monitoria.html', {'form': form})

def cadastrar_iniciacao_cientifica(request):
    if request.method == 'POST':
        form = IniciacaoCientificaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação Científica cadastrada com sucesso!')
            return redirect('listar_programas')
    else:
        form = IniciacaoCientificaForm()
    return render(request, 'apps/cadastrar_iniciacao.html', {'form': form})

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

class BaseCrudView:
    model = None  # definido pelas classes que herdam
    template_name = ''  # template padrão para reutilizar
    success_url = reverse_lazy('home')  # Redireciona após CRUD

class IniciativaEstudantilListView(BaseCrudView, ListView):
    model = IniciativaEstudantil
    template_name = 'apps/iniciativas/iniciativa_list.html'

class IniciativaEstudantilDetailView(BaseCrudView, DetailView):
    model = IniciativaEstudantil
    template_name = 'apps/iniciativas/iniciativa_detail.html'

class IniciativaEstudantilCreateView(BaseCrudView, CreateView):
    model = IniciativaEstudantil
    fields = ['nome', 'descricao', 'responsavel', 'site']
    template_name = 'apps/iniciativas/iniciativa_form.html'

class IniciativaEstudantilUpdateView(BaseCrudView, UpdateView):
    model = IniciativaEstudantil
    fields = ['nome', 'descricao', 'responsavel', 'site']
    template_name = 'apps/iniciativas/iniciativa_form.html'

class IniciativaEstudantilDeleteView(BaseCrudView, DeleteView):
    model = IniciativaEstudantil
    template_name = 'apps/iniciativas/iniciativa_confirm_delete.html'

class FavoritoListView(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = 'apps/favoritos.html'
    context_object_name = 'favoritos'
    
    def get_queryset(self):
        """
        Filtra os favoritos do usuário logado e, opcionalmente, por tipo de objeto.
        """
        queryset = Favorito.objects.filter(user=self.request.user)
        tipo = self.request.GET.get('tipo', None)
        if tipo:
            queryset = queryset.filter(content_type__model=tipo)  # Ajuste no campo de filtro

        return queryset

    def post(self, request, *args, **kwargs):
        """
        Lida com a ação de desfavoritar. Remove o favorito e exibe uma mensagem de confirmação.
        """
        favorito_id = request.POST.get('favorito_id')
        favorito = Favorito.objects.filter(id=favorito_id, user=request.user).first()
        if favorito:
            favorito.delete()
            messages.success(request, "Favorito removido com sucesso!")
        else:
            messages.error(request, "Favorito não encontrado ou não pertence a você.")

        # Retorna à página de favoritos
        return redirect('apps/favoritos.html')
