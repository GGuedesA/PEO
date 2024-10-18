# Generated by Django 5.1.2 on 2024-10-17 23:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0005_alter_usuario_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_aula', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tempo_aula', models.PositiveSmallIntegerField()),
                ('pago', models.BooleanField(default=False)),
                ('data_aula', models.DateTimeField()),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
                ('situacao', models.IntegerField(choices=[(0, 'Aguardando confirmação'), (1, 'Confirmado'), (2, 'Aguardando pagamento'), (3, 'Agendado'), (4, 'Finalizado'), (5, 'Cancelado')], default=0)),
                ('educador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aulas', to='sistema.educador')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aulas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]