from django.contrib.auth.backends import BaseBackend
from sistema.models import Usuario
from django.contrib.auth.hashers import check_password

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, nome_usuario=None, senha=None, **kwargs):
        try:
            # Autentica pelo campo `nome_usuario`
            print(nome_usuario)
            usuario = Usuario.objects.get(nome_usuario=nome_usuario)
            
            # Verifica a senha usando `check_password`
            print("Cheguei até aqui, auth tá indo certo", senha, usuario.password, check_password(senha, usuario.password))
            if check_password(senha, usuario.password):
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
