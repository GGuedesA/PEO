from django.urls import path
from sistema import views

app_name = 'sistema'

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('educadores/', views.educadores, name='educadores'),
    path('educadores/buscar/', views.buscar, name='buscar'),
    path('educador/<int:_id>/', views.educador, name='educador'),
    path('educador/<int:_id>/editar', views.editar_educador, name='editar_educador'),
    
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/educador', views.criar_educador, name='cadastro_educador'),
    
    path('usuario/<int:_id>/', views.dados_usuario, name='dados_usuario'),
    path('usuario/<int:_id>/editar', views.editar_usuario, name='editar_usuario'),
    
    path('pagamentocartao/', views.pagamentocartao, name='pagamentocartao'),
]
