from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from rest_framework.exceptions import NotFound

from .models import Teacher
from .serializers import TeacherSerializer
from .permissions import TeacherListPermission

class TeacherList(APIView):
    permission_classes = (TeacherListPermission,)
    
    def get(self, request):
        q = request.query_params.get("q", "")
        teachers = Teacher.objects.filter(description__icontains=q)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return Response(
                    {"detail": "Usuário com este email já existe."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"detail": "Erro ao processar a solicitação."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def put(self, request):
        if not isinstance(request.user, Teacher):
            return Response(
                {"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN
            )
        teacher_instance = request.user
        serializer = TeacherSerializer(teacher_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TeacherDetail(APIView):
    def get(self, request, pk):
        teacher = Teacher.objects.filter(pk=pk).first()
        if teacher is None:
            raise NotFound(detail="Professor não encontrado.")
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    