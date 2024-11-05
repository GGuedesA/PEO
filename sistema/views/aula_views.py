import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from sistema.models import *
from sistema.forms import ValorAulaForm

# o nome Lista aqui se refere caso seja para listar 
# como estudante ou como educador, 
# 0 para estudante e 1 para educador
@login_required
def listar_aulas(request, lista=None):
    usuario = request.user

    if(usuario.eh_educador): 
        lista = '1' if lista != '0' else '0'
    else:
        if(lista != None):
            return redirect('sistema:easter_egg')
        lista = '0'

    if lista == '0':
        aulas = Aula.objects.filter(estudante=usuario)
    else:
        aulas = Aula.objects.filter(educador__usuario=usuario)

    situacoes_styles = get_situacoes_styles()
    situacoes = get_situacoes_choices()
    aulas_por_situacao = {chave: [] for chave in situacoes.keys()}

    for aula in aulas:
        aulas_por_situacao[aula.situacao].append(aula)

    context = {
        'aulas_por_situacao': aulas_por_situacao,
        'situacoes': situacoes,
        'situacoes_styles': situacoes_styles,
        'lista': lista,
    }
    return render(request, 'sistema/listar_aulas.html', context)

@login_required
def dados_aula(request, _id):
    aula = get_object_or_404(Aula, id=_id)
    if aula.estudante != request.user and aula.educador.usuario != request.user:
        return redirect('sistema:easter_egg')
    situacoes_styles = get_situacoes_styles()
    situacoes = get_situacoes_choices()
    estudante = aula.estudante
    educador = aula.educador
    context = {
        'aula': aula,
        'estudante': estudante,
        'educador': educador, 
        'situacoes': situacoes,
        'situacoes_styles': situacoes_styles, 
    }
    return render(request, 'sistema/dados_aula.html', context)

@login_required
def muda_situacao(request, _id, situacao):
    aula = get_object_or_404(Aula, id=_id)
    if aula.estudante != request.user and aula.educador.usuario != request.user:
        return redirect('sistema:easter_egg')
    aula.situacao = situacao
    aula.save()
    return redirect('sistema:dados_aula', _id=aula.pk)

@login_required
def definir_valor(request, _id):
    aula = get_object_or_404(Aula, id=_id)
    if aula.educador.usuario != request.user:
        return redirect('sistema:easter_egg')
    
    if request.method == 'POST':
        form = ValorAulaForm(request.POST, instance=aula, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('sistema:dados_aula', _id=aula.pk)

    context = {
        'aula': aula,
        'form': ValorAulaForm(instance=aula, valor_inicial=aula.educador.valor_aula),
        'form_action': reverse('sistema:definir_valor', args=(_id,)),  # Necessário para recarregar o formulário após o envio
    }
    return render(request, 'sistema/definir_valor_aula.html', context)

@login_required
def realizar_pagamento(request, _id):
    aula = get_object_or_404(Aula, id=_id)
    usuario = request.user
    if aula.estudante != usuario:
        return redirect('sistema:easter_egg')
    
    pode_pagar = False
    if aula.valor_aula <= usuario.saldo:
        pode_pagar = True
    
    if request.method == 'POST':
        aula.pago = True
        aula.situacao += 1
        usuario.saldo -= aula.valor_aula
        educador = aula.educador
        educador.usuario.saldo += aula.valor_aula
        usuario.save()
        educador.usuario.save()
        aula.save()
        return redirect('sistema:dados_aula', _id=aula.pk)
    
    context = {
        'usuario': usuario,
        'pode_pagar': pode_pagar,
    }
    return render(request, 'sistema/pagar_aula.html', context)


@login_required
def iniciar_aula_jitsi(request, _id):
    aula = get_object_or_404(Aula, id=_id)
    if aula.estudante != request.user and aula.educador.usuario != request.user:
        return redirect('sistema:easter_egg')
    
    # Gera o nome da sala baseado no ID da aula ou outro identificador único
    nome_sala = f"aula-{aula.id}_{uuid.uuid4().hex[:8]}"

    # Atualiza a situação da aula e a URL da sala
    aula.situacao += 1
    aula.sala_url = f"https://meet.jit.si/{nome_sala}"
    aula.save()

    # Redireciona de volta para a página de dados da aula ou qualquer página onde o botão será exibido
    return redirect('sistema:dados_aula', _id=aula.pk)


@login_required
def entrar_aula(request, _id):
    aula = get_object_or_404(Aula, id=_id)
    return redirect(aula.sala_url)

