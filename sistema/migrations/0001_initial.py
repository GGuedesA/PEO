# Generated by Django 5.1.2 on 2024-10-14 19:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_usuario', models.CharField(max_length=60, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=255)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('cpf', models.CharField(max_length=14)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ativo', models.BooleanField(default=True)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Educador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minibio', models.CharField(default='Sem resumo', max_length=255)),
                ('descricao', models.TextField(default='Sem descrição')),
                ('tempo_aula', models.PositiveIntegerField(default=60)),
                ('valor_aula', models.DecimalField(decimal_places=2, default=50, max_digits=5)),
                ('dias_horas_preferidas', models.TextField(blank=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('areas', models.ManyToManyField(related_name='educadores', to='sistema.area')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.usuario')),
            ],
            options={
                'verbose_name_plural': 'educadores',
            },
        ),
    ]
