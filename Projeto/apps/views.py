from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Perfil, Evento
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

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
