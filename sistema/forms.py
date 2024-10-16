from sistema.models import *
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
        validators=[RegexValidator(r'^\d{1,11}$')],
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

    class Meta:
        model = Usuario
        fields = (
            'nome_usuario', 'nome',  
            'email', 'data_nascimento', 'telefone', 'cpf',
            'senha', 'confirmar_senha', 'imagem',
        )

    def clean(self):
        super().clean()  # Chama o método clean da superclasse
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        if senha != confirmar_senha:
            self.add_error('confirmar_senha', ValidationError('As senhas não coincidem'))
        return super().clean()

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf_validate(cpf):  # Supondo que você tenha essa função de validação
            self.add_error('cpf', ValidationError('CPF inválido'))
        return cpf
    
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
        # Usa set_password para garantir que a senha seja salva de forma segura
        usuario.set_password(self.cleaned_data['senha'])  # Define a senha usando o método correto
        if commit:
            usuario.save()
        return usuario


class EducadorForm(forms.ModelForm):
    minibio = forms.CharField(max_length=255, required=False, initial='Sem resumo')
    descricao = forms.CharField(widget=forms.Textarea, required=False, initial='Sem descrição')
    tempo_aula = forms.IntegerField(min_value=1, initial=60)
    valor_aula = forms.DecimalField(max_digits=5, decimal_places=2, initial=50)
    dias_horas_preferidas = forms.CharField(required=False, initial='todos:13-17')
    
    # ManyToManyField de áreas, deve garantir que o queryset esteja correto
    areas = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), required=False)

    class Meta:
        model = Educador
        fields = (
            'minibio', 'descricao', 'tempo_aula', 
            'valor_aula', 'dias_horas_preferidas', 'areas',
        )
        
class LoginForm(forms.Form):
    nome_usuario = forms.CharField(label="Nome de usuário")
    senha = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['nome_usuario'].widget.attrs.update({'placeholder': 'Nome de usuário'})
        self.fields['senha'].widget.attrs.update({'placeholder': 'Senha'})
