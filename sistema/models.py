from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, nome_usuario, password=None, **extra_fields):
        if not nome_usuario:
            raise ValueError('O campo nome de usuário é obrigatório')
        usuario = self.model(nome_usuario=nome_usuario, **extra_fields)
        usuario.set_password(password)  # Define a senha do usuário
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, nome_usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(nome_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nome_usuario = models.CharField(max_length=60, unique=True)
    email = models.EmailField(blank=True, max_length=254, null=True, unique=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)   
    imagem = models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m/%d/')
    eh_educador = models.BooleanField(default=False)
    saldo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Campos necessários para o Django
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'nome_usuario'  # Define o campo que será usado para login
    PASSWORD_FIELD = 'password'

    def __str__(self):
        return f'{self.nome_usuario}'


class Area(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Educador(models.Model):
    class Meta:
        verbose_name_plural = "educadores"
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, related_name="educador")
    minibio = models.CharField(max_length=255, default='Sem resumo')
    descricao = models.TextField(default='Sem descrição')
    tempo_aula = models.PositiveIntegerField(default=60)
    valor_aula = models.DecimalField(default=50, max_digits=5, decimal_places=2)
    dias_horas_preferidas = models.TextField(null=True, blank=True, default='todos:13-17')
    ativo = models.BooleanField(default=True)   
    areas = models.ManyToManyField(Area, related_name='educadores')

    def __str__(self):
        return f"{self.usuario.nome_usuario} {self.usuario.cpf}"
    
    def save(self, *args, **kwargs):
        self.usuario.eh_educador = True
        super(Educador, self).save(*args, **kwargs)
        self.usuario.save()
    

def get_situacoes():
    # Essa função define as situações das aulas, na esquerda a forma "human readable" do choices e na direita ficam 
    # as tags css que serão renderizadas, estilize elas através do arquivo styles-aulas.css dentro do static global
    return {
        'Aguardando confirmação'   : 'categoria-confirmar-educador', 
        'Confirmado pelo educador' : 'categoria-confirmar-estudante',
        'Aguardando pagamento'     : 'categoria-pagar',
        'Agendado'                 : 'categoria-agendado',
        'Iniciado'                 : 'categoria-iniciado',
        'Finalizado'               : 'categoria-finalizado',
        'Negado pelo educador'     : 'categoria-negado-educador',
        'Negado pelo estudante'    : 'categoria-negado-estudante',
        'Cancelado pelo educador'  : 'categoria-cancelado',
        'Cancelado pelo estudante' : 'categoria-cancelado',
    } 

def get_situacoes_choices():
    # essa função pega a de cima e gera um dicionário como o indice como chave e o human readable como valor
    return {i: chave for i, chave in enumerate(get_situacoes())}

def get_situacoes_styles():
    # essa função pega a de cima e gera um dicionário como o indice como chave e as tags css como valor
    return {i: valor for i, valor in enumerate(get_situacoes().values())}
    
class Aula(models.Model):
    estudante = models.ForeignKey(Usuario, on_delete=models.RESTRICT, related_name="aulas")
    educador = models.ForeignKey(Educador, on_delete=models.RESTRICT, related_name="aulas")
    valor_aula = models.DecimalField(max_digits=6, decimal_places=2)
    tempo_aula = models.PositiveSmallIntegerField()
    pago = models.BooleanField(default=False)
    data_aula = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    situacao = models.IntegerField(choices=get_situacoes_choices, default=0,)
    class Meta:
        constraints = [
            # Impedir sobreposição de aulas para o mesmo estudante
            models.UniqueConstraint(
                fields=['estudante', 'data_aula'],
                name='unique_aula_estudante_horario',
                condition=Q(
                    # proibe o caso de "existe_inicio >= horario_inicio < existe_fim" para o estudante
                    Q(horario_inicio__gte=models.F('horario_inicio'), horario_inicio__lt=models.F('horario_fim')) |
                    # proibe o caso de "existe_inicio > horario_fim <= existe_fim" para o estudante
                    Q(horario_fim__gt=models.F('horario_inicio'), horario_fim__lte=models.F('horario_fim'))
                )
            ),
            # Impedir sobreposição de aulas para o mesmo educador
            models.UniqueConstraint(
                fields=['educador', 'data_aula'],
                name='unique_aula_educador_horario',
                condition=Q(
                    # proibe o caso de "existe_inicio >= horario_inicio < existe_fim" para o educador
                    Q(horario_inicio__gte=models.F('horario_inicio'), horario_inicio__lt=models.F('horario_fim')) |
                    # proibe o caso de "existe_inicio > horario_fim <= existe_fim" para o educador
                    Q(horario_fim__gt=models.F('horario_inicio'), horario_fim__lte=models.F('horario_fim'))
                )
            )
        ]
        
    def __str__(self):
        return f"Estudante: {self.estudante.nome} | Educador: {self.educador.usuario.nome}  dia: {self.data_aula} das {self.horario_inicio} até {self.horario_fim}"
    