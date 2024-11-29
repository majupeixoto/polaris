from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, Evento, GrupoEstudo, ProgramaOficial, Voluntariado, Monitoria, IniciacaoCientifica, IniciativaEstudantil, Favorito, FAQ, ProgramaOficial
from .forms import GrupoEstudoForm, EventoForm, PerfilForm, VoluntariadoForm, MonitoriaForm, IniciacaoCientificaForm, ProgramaOficialForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from unidecode import unidecode
from django.core.paginator import Paginator

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
'''
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
'''
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
            # Cria o evento sem os campos ManyToMany
            evento = form.save(commit=False)
            evento.save()  # Salva o evento para gerar o ID necessário
            
            # Associar os campos ManyToMany
            if 'participantes' in form.cleaned_data:
                participantes = form.cleaned_data['participantes']
                if participantes:
                    evento.participantes.set(participantes)

            # Atualizar o campo tags diretamente
            if 'tags' in form.cleaned_data:
                evento.tags = ', '.join(form.cleaned_data['tags'])  # Converte a lista de tags em uma string separada por vírgulas
                evento.save()  # Salva o evento novamente para garantir que a associação seja persistida

            messages.success(request, "Evento cadastrado com sucesso!")
            return redirect('visualizar_evento', evento_id=evento.id)
        else:
            messages.error(request, "Erro ao cadastrar evento. Verifique os dados e tente novamente.")
    else:
        form = EventoForm()

    return render(request, 'apps/cadastrar_evento.html', {'form': form})

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
    return render(request, 'apps/home_aluno.html', {'eventos': eventos, 'user': user})


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

def listar_programas(request):
    monitorias = Monitoria.objects.all()
    voluntariados = Voluntariado.objects.all()
    iniciacoes_cientificas = IniciacaoCientifica.objects.all()
    
    context = {
        'monitorias': monitorias,
        'voluntariados': voluntariados,
        'iniciacoes_cientificas': iniciacoes_cientificas,
    }
    
    return render(request, 'apps/listar_programas.html', context)

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
            messages.error(request, 'Erro ao cadastrar o voluntariado. Verifique os dados.')
    else:
        form = VoluntariadoForm()
    return render(request, 'apps/cadastrar_voluntariado.html', {'form': form})

def cadastrar_monitoria(request):
    if request.method == 'POST':
        form = MonitoriaForm(request.POST)
        if form.is_valid():
            monitoria = form.save(commit=False)  # Salva sem persistir no BD ainda

            # Converter 'cadeiras_requeridas' e 'requisitos' para listas (dividindo a string por vírgula)
            cadeiras_input = form.cleaned_data.get('cadeiras_requeridas', '')
            requisitos_input = form.cleaned_data.get('requisitos', '')
            
            # Se houver valores, transforma em lista separando por vírgula
            monitoria.cadeiras_requeridas = [cadeira.strip() for cadeira in cadeiras_input.split(',')] if cadeiras_input else []
            monitoria.requisitos = [requisito.strip() for requisito in requisitos_input.split(',')] if requisitos_input else []

            # Salvar o objeto no banco
            monitoria.save()

            messages.success(request, 'Monitoria cadastrada com sucesso!')
            return redirect('listar_programas')
        else:
            messages.error(request, 'Erro ao cadastrar a monitoria. Verifique os dados.')
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
            messages.error(request, 'Erro ao cadastrar a Iniciação Científica. Verifique os dados.')
    else:
        form = IniciacaoCientificaForm()
    return render(request, 'apps/cadastrar_iniciacao.html', {'form': form})

@login_required
def visualizar_programa(request, programa_id):
    programa = get_object_or_404(ProgramaOficial, id=programa_id)
    
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

@login_required
def visualizar_evento(request, evento_id):
    # Obtém o evento pelo ID
    evento = get_object_or_404(Evento, id=evento_id)

    # Obtém o tipo de conteúdo do modelo Evento
    evento_content_type = ContentType.objects.get_for_model(Evento)

    # Verifica se o evento está nos favoritos do usuário atual
    favoritado = Favorito.objects.filter(
        user=request.user,
        content_type=evento_content_type,
        object_id=evento.id
    ).exists()

    # Adiciona a propriedade favoritado ao evento
    evento.favoritado = favoritado

    return render(request, 'apps/visualizar_evento.html', {'evento': evento})


@login_required
def favoritar_evento(request):
    if request.method == 'POST':
        evento_id = request.POST.get('evento_id')
        action = request.POST.get('action')

        # Obtém o evento e seu ContentType
        evento = get_object_or_404(Evento, id=evento_id)
        evento_content_type = ContentType.objects.get_for_model(Evento)

        if action == 'favoritar':
            # Cria o favorito
            Favorito.objects.get_or_create(
                user=request.user,
                content_type=evento_content_type,
                object_id=evento.id
            )
        elif action == 'desfavoritar':
            # Remove o favorito
            Favorito.objects.filter(
                user=request.user,
                content_type=evento_content_type,
                object_id=evento.id
            ).delete()

        # Retorna uma resposta JSON indicando sucesso e o novo estado do evento
        return JsonResponse({
            'success': True,
            'favoritado': action == 'favoritar'
        })

class IniciativaEstudantilListView(ListView):
    model = IniciativaEstudantil
    template_name = 'apps/iniciativas/iniciativa_list.html'
    context_object_name = 'iniciativas'

class IniciativaEstudantilDetailView(DetailView):
    model = IniciativaEstudantil
    template_name = 'apps/iniciativas/iniciativa_detail.html'

class IniciativaEstudantilCreateView(CreateView):
    model = IniciativaEstudantil
    fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'objetivo', 'docente_supervisor', 'site']
    template_name = 'apps/iniciativas/iniciativa_form.html'
    success_url = 'apps/sucesso.html'

class IniciativaEstudantilUpdateView(UpdateView):
    model = IniciativaEstudantil
    fields = ['titulo', 'descricao', 'status_inscricoes', 'tags', 'objetivo', 'docente_supervisor', 'site']
    template_name = 'apps/iniciativas/iniciativa_form.html'
    success_url = 'apps/sucesso.html'

class IniciativaEstudantilDeleteView(DeleteView):
    model = IniciativaEstudantil
    template_name = 'apps/iniciativas/iniciativa_confirm_delete.html'
    success_url = 'apps/sucesso.html'

class FavoritoListView(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = 'apps/favoritos.html'
    context_object_name = 'favoritos'

    def get_queryset(self):
        queryset = Favorito.objects.filter(user=self.request.user)
        tipo = self.request.GET.get('tipo', None)
        q = self.request.GET.get('q', None)

        if tipo:
            queryset = queryset.filter(content_type__model=tipo)  # tipo de objeto, se fornecido
        
        if q:
            queryset = queryset.filter(
                Q(objeto_favoritado__nome__icontains=q) |  # nome do objeto
                Q(objeto_favoritado__descricao__icontains=q)  # descrição
            )

        return queryset

    def post(self, request, *args, **kwargs):
        """
        Lida com a ação de desfavoritar. Remove o favorito diretamente.
        """
        favorito_id = request.POST.get('favorito_id')
        Favorito.objects.filter(id=favorito_id, user=request.user).delete()
        
        return redirect(reverse('favoritos'))

class ProgramaListView(ListView):
    model = ProgramaOficial
    template_name = 'apps/programas/programa_list.html'
    context_object_name = 'programas'

class ProgramaDetailView(DetailView):
    model = ProgramaOficial
    template_name = 'apps/programas/programa_detail.html'
    context_object_name = 'programa'

class ProgramaCreateView(CreateView):
    model = ProgramaOficial
    form_class = ProgramaOficialForm
    template_name = 'apps/programas/programa_form.html'
    success_url = 'apps/sucesso.html'

class ProgramaUpdateView(UpdateView):
    model = ProgramaOficial
    form_class = ProgramaOficialForm
    template_name = 'apps/programas/programa_form.html'
    success_url = 'apps/sucesso.html'

class ProgramaDeleteView(DeleteView):
    model = ProgramaOficial
    template_name = 'apps/programas/programa_confirm_delete.html'
    success_url = reverse_lazy('programa_list')


def search_results(request):
    query = request.GET.get('q', '').strip()
    query = unidecode(query.lower())
    obj_type = request.GET.get('type', '').strip()  # tipo selecionado
    results = []

    if query:
        # condições para cada modelo
        if obj_type == 'evento' or not obj_type:
            results += list(Evento.objects.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ))
        if obj_type == 'grupoestudo' or not obj_type:
            results += list(GrupoEstudo.objects.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ))
        if obj_type == 'voluntariado' or not obj_type:
            results += list(Voluntariado.objects.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ))
        if obj_type == 'monitoria' or not obj_type:
            results += list(Monitoria.objects.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ))
        if obj_type == 'iniciacao' or not obj_type:
            results += list(IniciacaoCientifica.objects.filter(
                Q(titulo__icontains=query) | Q(descricao__icontains=query)
            ))
        if obj_type == 'iniciativa' or not obj_type:
            results += list(IniciativaEstudantil.objects.filter(
                Q(nome__icontains=query) | Q(descricao__icontains=query)
            ))
    else:
        results = []

    # paginação
    from django.core.paginator import Paginator
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'apps/search_results.html', {
        'query': query,
        'type': obj_type,
        'page_obj': page_obj,
    })


def faq_view(request):
    query = request.GET.get('q', '')
    faqs = FAQ.objects.all()

    if query:
        faqs = faqs.filter(Q(pergunta__icontains=query) | Q(resposta__icontains=query))

    return render(request, 'apps/faq.html', {'faqs': faqs, 'query': query})
        

@login_required
def alterar_evento(request, evento_id):
    user = request.user
    if not user.is_superuser:  # Apenas superusuários podem alterar eventos
        messages.warning(request, "Você precisa ser um superusuário para alterar este evento.")
        return redirect('visualizar_evento', evento_id=evento_id)

    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento alterado com sucesso!")
            return redirect('visualizar_evento', evento_id=evento.id)
        else:
            messages.error(request, "Erro ao alterar o evento.")
    else:
        form = EventoForm(instance=evento)

    return render(request, 'apps/alterar_evento.html', {'form': form, 'evento': evento})

@login_required
def excluir_evento(request, evento_id):
    user = request.user
    if not user.is_superuser:  # Apenas superusuários podem excluir eventos
        messages.warning(request, "Você precisa ser um superusuário para excluir este evento.")
        return redirect('visualizar_evento', evento_id=evento_id)

    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        evento.delete()
        messages.success(request, "Evento excluído com sucesso!")
        return redirect('listar_eventos')

    return render(request, 'apps/excluir_evento.html', {'evento': evento})

@login_required
def search_favorites(request):
    query = request.GET.get('q', '')
    obj_type = request.GET.get('type', '')
    user = request.user
    results = []

    if obj_type:
        # filtra favoritos de um tipo específico
        content_type = ContentType.objects.filter(model=obj_type).first()
        if content_type:
            model = content_type.model_class()
            favoritos = user.favoritos.filter(content_type=content_type)
            objects = model.objects.filter(
                Q(id__in=[fav.object_id for fav in favoritos]) &
                Q(titulo__icontains=query)
            )
            results.extend(objects)
    else:
        favoritos = user.favoritos.all()
        for fav in favoritos:
            model = fav.content_type.model_class()
            obj = model.objects.filter(id=fav.object_id, titulo__icontains=query).first()
            if obj:
                results.append(obj)

    context = {
        'results': results,
        'query': query,
        'obj_type': obj_type,
    }
    return render(request, 'favorites_search_results.html', context)