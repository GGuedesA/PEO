from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from sistema.forms import *

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome_usuario = form.cleaned_data.get('nome_usuario')
            senha = form.cleaned_data.get('senha')
            usuario = authenticate(request, nome_usuario=nome_usuario, senha=senha)
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