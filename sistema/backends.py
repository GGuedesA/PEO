from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from sistema.models import Usuario
import re

class UsuarioBackend(BaseBackend):
    # Nome_usuario pode ser um email também
    def authenticate(self, request, nome_usuario=None, senha=None, **kwargs):
        try:
            rexp = r'^.+@.+\..+$'
            if re.match(rexp, nome_usuario):
                usuario = Usuario.objects.filter(email=nome_usuario).get()
            else:
                usuario = Usuario.objects.filter(nome_usuario=nome_usuario).get()
            if check_password(senha, usuario.password):
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
