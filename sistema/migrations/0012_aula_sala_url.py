# Generated by Django 5.1.2 on 2024-11-05 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0011_usuario_saldo_alter_educador_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='aula',
            name='sala_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
