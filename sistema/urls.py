from django.urls import path
from sistema import views

app_name = 'sistema'

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('minhas_aulas/', views.listar_aulas, name='minhas_aulas'),
    path('minhas_aulas/<lista>/', views.listar_aulas, name='minhas_aulas'),
    path('aula/<int:_id>/', views.dados_aula, name='dados_aula'), 

    path('really?/', views.easter_egg, name='easter_egg'),

    path('educadores/', views.educadores, name='educadores'),
    path('educadores/buscar/', views.buscar, name='buscar'),
    path('educador/<int:_id>/', views.educador, name='educador'),
    path('educador/<int:_id>/editar/', views.editar_educador, name='editar_educador'),
    path('educador/<int:educador_id>/contratar/', views.cadastrar_aula, name='cadastrar_aula'),
    
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/educador/', views.criar_educador, name='cadastro_educador'),
    
    path('usuario/<int:_id>/', views.dados_usuario, name='dados_usuario'),
    path('usuario/<int:_id>/editar/', views.editar_usuario, name='editar_usuario'),

    path('mudar_situacao_aula/<int:_id>/<int:situacao>/', views.muda_situacao, name='mudar_situacao'),
    path('realizar_pagamento/<int:_id>/', views.realizar_pagamento, name='pagar_aula'),
    path('definir_valor_aula/<int:_id>/', views.definir_valor, name='definir_valor'),
    
    path('recarga/', views.recarga, name='recarga'),
]
