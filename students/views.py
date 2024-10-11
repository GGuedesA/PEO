from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import IntegrityError
from rest_framework.exceptions import NotFound

from .models import Student
from .serializers import StudentSerializer
from .permissions import StudentListPermission

class StudentList(APIView):
    permission_classes = (StudentListPermission,)
    
    def get(self, request):
        q = request.query_params.get("q", "")
        students = Student.objects.filter(description__icontains=q)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return Response(
                    {"detail": "Usuário com este email já existe."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"detail": "Erro ao processar a solicitação"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    
    def put(self, request):
        if not isinstance(request.user, Student):
            return Response(
                {"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN
            )
        student_instance = request.user
        serializer = StudentSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StudentDetail(APIView):
    def get(self, request, pk):
        student = Student.objects.filter(pk=pk).first()
        if student is None:
            raise NotFound(detail="Aluno não encontrado.")
        serializer = StudentSerializer(student)
        return Response(serializer.data)