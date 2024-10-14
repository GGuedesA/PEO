from django.shortcuts import render, get_object_or_404
from sistema.models import *

def index(request):
    return render(request, 'sistema/index.html', )

def educadores(request):
    educadores = Educador.objects.all().filter(ativo=True)
    context = {
        'educadores': educadores
    }
    return render(request, 'sistema/educadores.html', context)

def buscar(request):
    busca = request.GET['q']
    print("buscando:", busca)
    educadores = Educador.objects.all().filter(ativo=True)
    context = {
        'educadores': educadores
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