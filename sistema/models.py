from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class Area(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class UsuarioManager(BaseUserManager):
    def create_user(self, nome_usuario, senha=None, **extra_fields):
        if not nome_usuario:
            raise ValueError('O nome de usuário é obrigatório')
        usuario = self.model(nome_usuario=nome_usuario, **extra_fields)
        if senha:
            usuario.set_password(senha)
        else:
            raise ValueError('A senha é obrigatória')
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nome_usuario, senha=None, **extra_fields):
        """Cria e salva um superusuário."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusuário precisa ter is_superuser=True.')
        return self.create_user(nome_usuario, senha, **extra_fields)
    

class Usuario(AbstractBaseUser, PermissionsMixin):
    nome_usuario = models.CharField(max_length=60, unique=True)
    email = models.EmailField(blank=True, max_length=254, null=True, unique=True)
    nome = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)   
    imagem = models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m/%d/')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'nome_usuario'
    REQUIRED_FIELDS = ['email', 'cpf']
    
    def __str__(self):
        return f'{self.nome_usuario}'


class Educador(models.Model):
    class Meta:
        verbose_name_plural = "educadores"
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    minibio = models.CharField(max_length=255, default='Sem resumo')
    descricao = models.TextField(default='Sem descrição')
    tempo_aula = models.PositiveIntegerField(default=60)
    valor_aula = models.DecimalField(default=50, max_digits=5, decimal_places=2)
    dias_horas_preferidas = models.TextField(null=True, blank=True, default='todos:13-17')
    ativo = models.BooleanField(default=True)   
    areas = models.ManyToManyField(Area, related_name='educadores')

    def __str__(self):
        return f"{self.usuario.nome_usuario} {self.usuario.cpf}"
    