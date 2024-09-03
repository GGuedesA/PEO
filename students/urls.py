from django.urls import path
from .views import StudentList, StudentDetail, MeView

app_name = "students"
urlpatterns = [
    path("alunos", StudentList.as_view(), name="list"),
    path("professores/<int:pk>", StudentDetail.as_view(), name="detail"),
    path("me/aluno", MeView.as_view(), name="me")
]
