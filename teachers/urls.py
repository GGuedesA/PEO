from django.urls import path
from .views import TeacherList, TeacherDetail, MeView

app_name = "teachers"
urlpatterns = [
    path("professores", TeacherList.as_view(), name="list"),
    path("professores/<int:pk>", TeacherDetail.as_view(), name="detail"),
    path("me/professor", MeView.as_view(), name="me")
]
