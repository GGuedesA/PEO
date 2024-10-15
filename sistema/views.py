from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from sistema.models import *

def index(request):
    return render(request, 'sistema/index.html', )

def educadores(request):
    educadores = Educador.objects.all().filter(ativo=True)
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
                    )
    paginator = Paginator(educadores, 25)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'valor_buscado': busca,
    }
    return render(request, 'sistema/educadores.html', context)

def educador(request, educador_id):
    single_educador = get_object_or_404(Educador, id=educador_id, ativo=True)
    areas = single_educador.areas.all()
    context = {
        'educador': single_educador,
        'areas': areas
    }
    return render(request, 'sistema/educador.html', context)