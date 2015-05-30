# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitucionEducativa',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=10, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('municipio', models.CharField(max_length=50)),
                ('zona', models.SmallIntegerField(choices=[('0', 'Urbana'), ('1', 'Urbana Marginal'), ('2', 'Rural'), ('3', 'Rural de Difícil Acceso')])),
                ('modalidad', models.SmallIntegerField(choices=[('0', 'Académica'), ('1', 'Técnica')])),
                ('orientacion_etnoeducativa', models.SmallIntegerField(choices=[('0', 'Ninguna'), ('1', 'Rom'), ('2', 'Afrocolombiana'), ('3', 'Indígena')])),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=15, serialize=False)),
                ('sexo', models.SmallIntegerField(choices=[('0', 'Masculino'), ('1', 'Femenino')])),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.IntegerField()),
                ('fijo', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SecretariaEducacion',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=10, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaderTeacher',
            fields=[
                ('persona_ptr', models.OneToOneField(serialize=False, parent_link=True, to='moodle.Persona', primary_key=True, auto_created=True)),
            ],
            bases=('moodle.persona',),
        ),
        migrations.AddField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institucioneducativa',
            name='secretaria',
            field=models.ForeignKey(to='moodle.SecretariaEducacion'),
        ),
        migrations.AddField(
            model_name='leaderteacher',
            name='institucion',
            field=models.ForeignKey(to='moodle.InstitucionEducativa'),
        ),
    ]
