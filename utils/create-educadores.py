import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice
import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_EDUCATORS = 30
NUMBER_OF_USERS = NUMBER_OF_EDUCATORS

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'projeto.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker
    from random import randint, uniform, sample
    from sistema.models import *
    from utils.custom_validators import cpf_generate
    from django.contrib.auth.hashers import make_password

    fake = faker.Faker('pt_BR')
    gerar_usuarios = True
    gerar_educadores = True

    resetar_banco = True
    if(resetar_banco):
        Area.objects.all().delete()
        Aula.objects.all().delete()
        Educador.objects.all().delete()
        Usuario.objects.all().delete()

    if(gerar_usuarios):
        users = []
        for _ in range(NUMBER_OF_USERS):
            profile = fake.profile()
            email = profile['mail']
            username = profile['username']
            nome = profile['name']
            nascimento = profile['birthdate']
            cpf = fake.cpf()
            senha = make_password('12345678')
            telefone = fake.phone_number()
            created = fake.date_this_year()

            users.append(
                Usuario(
                    nome_usuario=username,
                    nome=nome,
                    email=email,
                    telefone=telefone,
                    data_nascimento=nascimento,
                    cpf=cpf,
                    password=senha,
                    created_at=created
                )
            )
        if (len(users) > 0):
            for user in users:
                try:
                    Usuario.save(user)
                except:
                    ...
    
    if(gerar_educadores):
        usuarios_sem_educador = Usuario.objects.exclude(educador__isnull=False)
        areas = list(Area.objects.all())
        if(len(areas) < 1):
            areas_criar = [
                'Matemática', 
                'Português', 
                'Ciências', 
                'Cálculo diferencial', 
                'Cálculo 1',
                'História',
                'Geografia',
                'Inglês',
                'Religião',
                'Filosofia',
                'Estrutura de dados',
                'Biologia',
                'Química',
                'Arquitetura de software',
                'Sistemas distribuidos',
            ]
            areas_salvar = []
            for area in areas_criar:
                areas_salvar.append(Area(
                    nome=area
                ))
            Area.objects.bulk_create(areas_salvar)
        educadores = []
        areas = list(Area.objects.all())
        for i in range(NUMBER_OF_EDUCATORS if len(usuarios_sem_educador) >= NUMBER_OF_EDUCATORS else len(usuarios_sem_educador)):
            qtd_areas = randint(1, 6)
            minibio = fake.text(max_nb_chars=255)
            descricao = ' '.join(fake.sentences(nb=12))
            tempo = randint(40, 60)
            valor = uniform(50.00, 130.00)
            areas_educador = sample(areas, qtd_areas)
            novo_educador = Educador(
                    usuario=usuarios_sem_educador[i],
                    minibio=minibio,
                    descricao=descricao,
                    tempo_aula=tempo,
                    valor_aula=valor
                )
            novo_educador.save()
            novo_educador.areas.set(areas_educador)
    
    if resetar_banco:
        adm = Usuario(
            nome_usuario='admin',
            nome='Administrador',
            email='admin@email.com',
            telefone='(11) 99999-9999',
            data_nascimento=datetime(1990, 1, 1),
            cpf='12345678901',
            password=make_password('admin'),
            created_at=datetime.now(),
            is_superuser=True,
            is_staff=True
        )
        adm.save()
        educ1_user = Usuario(
            nome_usuario='educ1',
            nome='Educador 1 de testes',
            email='educ1@email.com',
            telefone='(11) 98765-4321',
            data_nascimento=datetime(1995, 6, 15),
            cpf='98765432109',
            password=make_password('educ1'),
            created_at=datetime.now()
        )
        educ1 = Educador(
            usuario=educ1_user,
            minibio='Minibio do educador 1',
            descricao='Descrição do educador 1',
            tempo_aula=45,
            valor_aula=80.00
        )
        educ1_user.save()
        educ1.save()