from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from sistema.forms import *

def cadastro(request):
    form_action = reverse('sistema:cadastro')
    if request.method == 'POST':
        form = UsuarioForm(request.POST, files=request.FILES)
        context = {
            'form': form,
            'form_action': form_action,
        }

        if(form.is_valid()):
            form.save()
            return redirect('sistema:educadores')

        return render(
            request,
            'sistema/form_usuario.html',
            context
        )
    
    context = {
        'form': UsuarioForm(),
        'form_action': form_action,
    }
    return render(request, 'sistema/form_usuario.html', context)

def editar_usuario(request, _id):
    usuario = get_object_or_404(Usuario, pk=_id, ativo=True)
    form_action = reverse('sistema:editar_usuario', args=(_id,))

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, files=request.FILES)
        context = {
            'form': form,
            'form_action': form_action,
        }

        if(form.is_valid()):
            usuario = form.save()
            return redirect('sistema:dados_usuario', _id=usuario.pk)

        return render(
            request,
            'sistema/form_usuario.html',
            context
        )
    
    context = {
        'form': UsuarioForm(instance=usuario),
        'form_action': form_action,
    }
    return render(request, 'sistema/form_usuario.html', context)

def criar_educador(request):
    form_action = reverse('sistema:cadastro_educador')  # URL da ação do formulário
    
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, files=request.FILES)
        educador_form = EducadorForm(request.POST)

        if usuario_form.is_valid() and educador_form.is_valid():
            # Salvando o usuário primeiro
            usuario = usuario_form.save()
            
            # Salvando o educador associado ao usuário
            educador = educador_form.save(commit=False)
            educador.usuario = usuario  # Associação do educador ao usuário
            educador.save()

            # Aqui, garantimos que o ManyToManyField 'areas' seja salvo corretamente
            educador_form.save_m2m()  # Salva os dados do ManyToManyField (áreas)

            return redirect('sistema:educador', educador.id)  # Redireciona para a página do educador

        # Se houver erros, renderiza o formulário com os erros
        context = {
            'form1': usuario_form,
            'form2': educador_form,
            'form_action': form_action,
        }
        return render(request, 'sistema/form_educador.html', context)

    # Requisição GET: exibe formulário vazio
    context = {
        'form1': UsuarioForm(),
        'form2': EducadorForm(),
        'form_action': form_action,
    }
    return render(request, 'sistema/form_educador.html', context)

def editar_educador(request, _id):
    # Obtendo o educador ou retornando 404 caso não exista
    educador = get_object_or_404(Educador, pk=_id, ativo=True)
    
    # Ação do formulário (a URL)
    form_action = reverse('sistema:editar_educador', args=(_id,))
    
    if request.method == 'POST':
        # Instância do formulário com os dados do POST e do objeto Educador existente
        usuario_form = UsuarioForm(request.POST, instance=educador.usuario, files=request.FILES)
        educador_form = EducadorForm(request.POST, instance=educador)
        
        context = {
            'form1': usuario_form,
            'form2': educador_form,
            'form_action': form_action,
        }

        if usuario_form.is_valid() and educador_form.is_valid():
            # Salvando o usuário associado ao educador
            usuario = usuario_form.save()

            # Salvando o educador e associando o usuário (embora já esteja associado)
            educador = educador_form.save(commit=False)
            educador.usuario = usuario  # Garantindo que o educador permaneça associado ao usuário
            educador.save()

            # Salvando o campo ManyToMany (áreas)
            educador_form.save_m2m()

            # Redirecionando para a página de detalhes do educador
            return redirect('sistema:educador', _id=educador.pk)

        # Caso os formulários tenham erros, renderizamos a página com os erros
        return render(request, 'sistema/form_educador.html', context)

    # Requisição GET: exibe o formulário preenchido com os dados atuais
    context = {
        'form1': UsuarioForm(instance=educador.usuario),
        'form2': EducadorForm(instance=educador),
        'form_action': form_action,
    }
    return render(request, 'sistema/form_educador.html', context)

@login_required
def cadastrar_aula(request, educador_id):
    educador = get_object_or_404(Educador, pk=educador_id, ativo=True)
    estudante_id = request.user.id
    estudante = get_object_or_404(Usuario, pk=estudante_id, ativo=True)
    form_action = reverse('sistema:cadastrar_aula', args=(educador_id,))
    if request.method == 'POST':
        form = AulaForm(request.POST, educador=educador, estudante=estudante)
        context = {
            'form': form,
            'form_action': form_action,
        }

        if(form.is_valid()):
            aula = form.save(commit=False)
            aula.educador = educador
            aula.estudante = estudante
            aula.save()
            # return redirect('sistema:aulas_educador', educador_id=educador.pk)
            return redirect('sistema:educador', _id=educador.pk)
        
        return render(
            request,
            'sistema/form_aula.html',
            context
        )
    
    context = {
        'form': AulaForm(educador=educador, estudante=estudante),
        'form_action': form_action,
    }
    return render(request, 'sistema/form_aula.html', context)