from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from sistema.models import Usuario
import re

class UsuarioBackend(BaseBackend):
    # Nome_usuario pode ser um email também
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            rexp = r'^.+@.+\..+$'
            if re.match(rexp, username):
                usuario = Usuario.objects.filter(email=username).get()
            else:
                usuario = Usuario.objects.filter(nome_usuario=username).get()
            if check_password(password, usuario.password):
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
