from django.contrib import admin

from sistema import models

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome',
    ordering = ('-id',)
    search_fields = 'id', 'nome',

@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = 'id', 'nome', 'nome_usuario', 'cpf',
    ordering = '-id',
    search_fields = 'id', 'nome', 'nome_usuario',
    list_per_page = 20
    list_editable = 'nome', 'nome_usuario',

@admin.register(models.Educador)
class EducadorAdmin(admin.ModelAdmin):
    list_display = 'id', 'usuario__nome', 'usuario__nome_usuario',
    search_fields = 'id', 'usuario__nome', 'usuario__nome_usuario',

@admin.register(models.Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = 'id', 'estudante__nome', 'estudante__nome_usuario', 'educador__usuario__nome', 'educador__usuario__nome_usuario',
    search_fields = 'id', 'estudante__nome', 'estudante__nome_usuario', 'educador__usuario__nome', 'educador__usuario__nome_usuario',
