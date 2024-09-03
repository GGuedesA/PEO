from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("api/", include("teachers.urls", namespace="teachers")),
    path("api/", include("students.urls", namespace="students")),
    path("api/auth/", include("accounts.urls", namespace="accounts")),
]
