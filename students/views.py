from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import StudentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Student
from .serializers import StudentSerializer
from .permissions import StudentListPermission

class StudentList(APIView):
    permission_classes = (StudentListPermission,)
    
    def get(self, request):
        q = request.query_params.get("q", "")
        teachers = Student.objects.filter(description__icontains=q)
        serializer = StudentSerializer(teachers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        serializer = StudentSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class StudentDetail(APIView):
    def get(self, request, pk):
        teacher = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(teacher)
        return Response(serializer.data)
    
class MeView(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = StudentSerializer(request.user)
        return Response(serializer.data)