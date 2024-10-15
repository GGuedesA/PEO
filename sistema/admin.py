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
