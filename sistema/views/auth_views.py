from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from sistema.forms import *

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome_usuario = form.cleaned_data.get('nome_usuario')
            print(nome_usuario)
            senha = form.cleaned_data.get('senha')
            print("Senha", senha)
            usuario = authenticate(request, nome_usuario=nome_usuario, senha=senha)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')  # Redirecionar para a home após o login
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'sistema/login.html', {'form': form})

def logout(request):
    context = {
    }
    return render(request, 'sistema/login.html', context)