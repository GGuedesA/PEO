from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from sistema.forms import *

def user_login(request):
    if(request.user.is_authenticated):
        return redirect('sistema:index')  # Redirecionar para a home após o login se o usuário já estiver logado

    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            nome_usuario = form.cleaned_data.get('nome_usuario')
            senha = form.cleaned_data.get('senha')
            usuario = authenticate(request, username=nome_usuario, password=senha)
            if usuario is not None:
                login(request, usuario)
                return redirect('sistema:index')  # Redirecionar para a home após o login
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'sistema/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('sistema:index')