from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenBlacklistView

from teachers.serializers import TeacherSerializer
from teachers.models import Teacher
from students.serializers import StudentSerializer
from students.models import Student

class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if isinstance(request.user, Teacher):
            serializer = TeacherSerializer(request.user)
        elif isinstance(request.user, Student):
            serializer = StudentSerializer(request.user)
        else:
            return Response({"detail": "Usuário desconhecido."}, statu=400)
        return Response(serializer.data)

class CustomTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_205_RESET_CONTENT)