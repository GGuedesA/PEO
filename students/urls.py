from django.urls import path
from .views import StudentList, StudentDetail

app_name = "students"
urlpatterns = [
    path("alunos", StudentList.as_view(), name="list"),
    path("professores/<int:pk>", StudentDetail.as_view(), name="detail"),
]
