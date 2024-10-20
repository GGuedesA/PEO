from sistema.models import *
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from utils.custom_validators import cpf_validate, valida_data_nascimento
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    nome_usuario = forms.CharField(
        label="Nome de usuário",
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome Usuário'}
        ),
    )
    nome = forms.CharField()
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    email = forms.EmailField(required=False)
    telefone = forms.CharField(
        required=False, 
        validators=[RegexValidator(r'^\d{1,11}$')],
        help_text='Entre apenas com os números'
    )
    cpf = forms.CharField(
        label="CPF",
        help_text="Entre apenas com os números"
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Insira sua senha'}
        ),
    )
    confirmar_senha = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme sua senha'}
        ),
    )
    imagem = forms.ImageField(
        required=False,
        label='Foto de perfil',                      
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        )
    )
    eh_educador = False

    class Meta:
        model = Usuario
        fields = (
            'nome_usuario', 'nome',  
            'email', 'data_nascimento', 'telefone', 'cpf',
            'senha', 'confirmar_senha', 'imagem',
        )

    def __init__(self, *args, **kwargs):
        self.eh_educador = kwargs.pop('eh_educador', False)
        super(UsuarioForm, self).__init__(*args, **kwargs)

    def clean(self):
        super().clean()  # Chama o método clean da superclasse
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        if senha != confirmar_senha:
            self.add_error('confirmar_senha', ValidationError('As senhas não coincidem'))
        return super().clean()

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if(len(cpf) > 14):
            self.add_error('cpf', ValidationError('Tamanho do CPF inserido muito grande'))
        #  Obtém os números do CPF e ignora outros caracteres
        cpf = [int(char) for char in str(cpf) if char.isdigit()]
        if not cpf_validate(cpf):  # Supondo que você tenha essa função de validação
            self.add_error('cpf', ValidationError('CPF inválido'))
        cpf_validado = ''.join(map(str, cpf))
        return cpf_validado
    
    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if not valida_data_nascimento(data_nascimento):  # Supondo que você tenha essa função de validação
            self.add_error('data_nascimento', ValidationError('Apenas para maiores de 18 anos'))
        return data_nascimento
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            self.add_error('email', ValidationError('Email já cadastrado'))
        return email
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.eh_educador = self.eh_educador
        print("To aqui, to aqui to aqui")
        print("To aqui, to aqui to aqui")
        print("To aqui, to aqui to aqui")
        print(self.eh_educador)
        print(usuario.eh_educador)
        # Usa set_password para garantir que a senha seja salva de forma segura
        usuario.set_password(self.cleaned_data['senha'])  # Define a senha usando o método correto
        if commit:
            usuario.save()
        return usuario


class EducadorForm(forms.ModelForm):
    minibio = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(
            attrs={'placeholder': 'Sem resumo'}
        )
    )
    descricao = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Sem Descrição'}
        ), 
        required=False, 
    )
    tempo_aula = forms.IntegerField(
        min_value=1, 
        initial=60, 
        help_text="Coloque o tempo de cada aula em minutos"
    )
    valor_aula = forms.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        initial=50
    )
    dias_horas_preferidas = forms.CharField(
        required=False, 
        label="Horários disponíveis",
        widget=forms.TextInput(attrs={'type': 'hidden'})
    )
    
    # ManyToManyField de áreas, deve garantir que o queryset esteja correto
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.all(), required=False
    )

    class Meta:
        model = Educador
        fields = (
            'minibio', 'tempo_aula', 
            'valor_aula', 'descricao', 'dias_horas_preferidas', 'areas',
        )
        
    def clean_dias_horas_preferidas(self):
        horarios = self.cleaned_data.get('dias_horas_preferidas')
        if not horarios or horarios == "":
            self.add_error(
                'dias_horas_preferidas',
                ValidationError('Insira pelo menos UM valor', code='invalid')
            )

        return horarios
        
class LoginForm(forms.Form):
    nome_usuario = forms.CharField(label="Nome de usuário")
    senha = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['nome_usuario'].widget.attrs.update({'placeholder': 'Nome de usuário', 'autofocus': 'autofocus'})
        self.fields['senha'].widget.attrs.update({'placeholder': 'Senha'})

class AulaForm(forms.ModelForm):
    data_aula = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}
    ))
    horario_inicio = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}
    ))
    horario_fim = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time'}
    ))
    valor_aula = None
    tempo_aula = None
    estudante = None
    educador = None

    class Meta:
        model = Aula
        fields = (
            'data_aula', 'horario_inicio', 'horario_fim',
        )
    
    def __init__(self, *args, **kwargs):
        self.estudante = kwargs.pop('estudante', None)
        self.educador = kwargs.pop('educador', None)
        self.valor_aula = self.educador.valor_aula
        super(AulaForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        data_aula = self.cleaned_data.get('data_aula')
        horario_inicio = self.cleaned_data.get('horario_inicio')
        horario_fim = self.cleaned_data.get('horario_fim')

         # Usa os atributos do formulário que foram passados no __init__
        educador = self.educador
        estudante = self.estudante

        if not educador or not estudante:
            raise ValidationError("Estudante ou Educador não fornecidos.")
        
        if horario_fim < horario_inicio:
            self.add_error(
                'horario_fim',
                ValidationError("O horário de término da aula não pode ser antes do horário de início.", code="invalid")
            )
        
        if horario_fim == horario_inicio:
            self.add_error(
                'horario_fim',
                ValidationError("A aula não pode durar zero minutos.", code="invalid")
            )
        
        self.valor_aula = educador.valor_aula

        conflicting_aulas_estudante = Aula.objects.filter(
            Q(
                Q(horario_inicio__lte=horario_inicio, horario_fim__gt=horario_inicio) 
                | 
                Q(horario_inicio__lt=horario_fim, horario_fim__gte=horario_fim)
            ),
            estudante=estudante,
            data_aula=data_aula,
        )

        # Verifica se já existe uma aula para o educador no mesmo dia e horário
        conflicting_aulas_educador = Aula.objects.filter(
            Q(
                Q(horario_inicio__lte=horario_inicio, horario_fim__gt=horario_inicio) 
                | 
                Q(horario_inicio__lt=horario_fim, horario_fim__gte=horario_fim)
            ),
            educador=educador,
            data_aula=data_aula,
        )

        if conflicting_aulas_estudante.exists():
            self.add_error(
                '',
                ValidationError("Você já possui uma aula para esse horário.", code="invalid")
            )
        if conflicting_aulas_educador.exists():
            self.add_error(
                '',
                ValidationError("Já existe uma aula agendada para esse educador neste horário.", code="invalid")
            )

        return super().clean()
    
    def clean_data_aula(self):
        data_aula = self.cleaned_data.get('data_aula')
        if data_aula < datetime.now().date():
            self.add_error('data_aula', ValidationError('A data da aula não pode ser menor que hoje'))
        if data_aula == datetime.now().date():
            self.add_error('data_aula', ValidationError('A data da aula deve ser marcada com pelo menos um dia de antecedência'))
        return data_aula
    
    def save(self, commit=True):
        aula = super(AulaForm, self).save(commit=False)

        # Garantir que os campos educador, estudante e valor_aula sejam preenchidos corretamente
        aula.educador = self.educador
        aula.estudante = self.estudante
        aula.valor_aula = self.educador.valor_aula
        dt1 = datetime.combine(datetime.now(), aula.horario_inicio)
        dt2 = datetime.combine(datetime.now(), aula.horario_fim)
        delta = dt2 - dt1
        aula.tempo_aula = delta.total_seconds() // 60

        if commit:
            aula.save()
        return aula
