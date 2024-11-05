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
    if request.user.is_authenticated and request.user.eh_educador:
        educadores = educadores.exclude(usuario=request.user)

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
                        usuario__nome__icontains=busca
                    ).order_by('-id')
    
    if request.user.is_authenticated and request.user.eh_educador:
        educadores = educadores.exclude(usuario=request.user)

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
    # if request.user.is_authenticated and request.user.eh_educador:
    #     if(request.user.educador == single_educador):
            # return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    areas = single_educador.areas.all()
    context = {
        'educador': single_educador,
        'areas': areas
    }
    return render(request, 'sistema/educador.html', context)

@login_required
def dados_usuario(request, _id):
    usuario = get_object_or_404(Usuario, id=_id, ativo=True)
    educador = None
    areas = []
    if usuario.eh_educador:
        educador = Educador.objects.get(usuario=usuario)
        areas = educador.areas.all()
    context = {
        'usuario': usuario,
        'eh_educador': usuario.eh_educador,
        'educador': educador,
        'areas': areas,
    }
    return render(request, 'sistema/dados_usuario.html', context)

def easter_egg(request):
    return render(request, 'sistema/easter_egg.html', )