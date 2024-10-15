from django.urls import path
from sistema import views

app_name = 'sistema'

urlpatterns = [
    path('', views.index, name='index'),
    path('educadores/', views.educadores, name='educadores'),
    path('educadores/buscar/', views.buscar, name='buscar'),
    path('educador/<int:educador_id>/', views.educador, name='educador'),
    path('pagamentocartao/', views.pagamentocartao, name='pagamentocartao'),
]
