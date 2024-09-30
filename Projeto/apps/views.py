from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Perfil

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
