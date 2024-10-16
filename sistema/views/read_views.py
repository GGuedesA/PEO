from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from sistema.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenBlacklistView

from sistema.serializers import UsuarioSerializer, EducadorSerializer

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

def dados_usuario(request, _id):
    usuario = get_object_or_404(Usuario, id=_id, ativo=True)
    context = {
        'usuario': usuario,
    }
    return render(request, 'sistema/dados_usuario.html', context)


def pagamentocartao(request):
    return render(request, 'sistema/pagamentocartao.html', )

class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            usuario = request.user  
            educador = Educador.objects.filter(usuario=usuario).first()

            if educador:
                serializer = EducadorSerializer(educador)
            else:
                serializer = UsuarioSerializer(usuario)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erro: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CustomTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_205_RESET_CONTENT)