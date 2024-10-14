from django.contrib import admin

from sistema import models

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Educador)
class EducadorAdmin(admin.ModelAdmin):
    ...
