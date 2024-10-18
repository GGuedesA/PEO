from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from sistema.models import *

@login_required
def index(request):
    return render(request, 'sistema/index.html', )

def educadores(request):
    educadores = Educador.objects.all().filter(ativo=True).order_by('-id')
    paginator = Paginator(educadores, 25)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'sistema/educadores.html', context)

def buscar(request):
    busca = request.GET.get('q', '').strip()
    if busca == '':
        return redirect('sistema:educadores')

    educadores = Educador.objects\
                    .filter(
                        ativo=True,
                        usuario__ativo=True
                    )\
                    .filter(
                        Q(usuario__nome_usuario__icontains=busca) | 
                        Q(usuario__nome__icontains=busca)
                    ).order_by('-id')
    paginator = Paginator(educadores, 25)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'valor_buscado': busca,
    }
    return render(request, 'sistema/educadores.html', context)

def educador(request, _id):
    single_educador = get_object_or_404(Educador, id=_id, ativo=True)
    areas = single_educador.areas.all()
    context = {
        'educador': single_educador,
        'areas': areas
    }
    return render(request, 'sistema/educador.html', context)

@login_required
def dados_usuario(request, _id):
    usuario = get_object_or_404(Usuario, id=_id, ativo=True)
    context = {
        'usuario': usuario,
    }
    return render(request, 'sistema/dados_usuario.html', context)


def pagamentocartao(request):
    return render(request, 'sistema/pagamentocartao.html', )

@login_required
def listar_aulas(request):
    usuario = request.user

    # Filtrar as aulas do usuário logado (tanto como estudante quanto como educador)
    aulas_como_estudante = Aula.objects.filter(estudante=usuario)
    print(aulas_como_estudante)
    aulas_como_educador = Aula.objects.filter(educador__usuario=usuario)
    print(aulas_como_educador)

    # Agrupar as aulas de acordo com a situação
    aulas_por_situacao = defaultdict(list)

    for aula in aulas_como_estudante:
        aulas_por_situacao[aula.situacao].append(aula)

    for aula in aulas_como_educador:
        aulas_por_situacao[aula.situacao].append(aula)

    # Passar o dicionário ao template
    print(aulas_por_situacao)
    context = {
        'aulas_por_situacao': aulas_por_situacao,
    }
    return render(request, 'sistema/listar_aulas.html', context)