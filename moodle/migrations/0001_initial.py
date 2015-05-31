# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import moodle.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
                ('titulo', models.CharField(max_length=60)),
                ('fecha_fin', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('porcentaje', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=60)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cohorte',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=60)),
                ('semestre', models.SmallIntegerField(choices=[(0, 'Febrero-Junio'), (1, 'Agosto-Diciembre')])),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=60)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
                ('area', models.ForeignKey(to='moodle.Area')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialAcademico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('tipoEstudio', models.PositiveSmallIntegerField(choices=[(0, 'Bachillerato'), (1, 'Pregrado'), (2, 'Posgrado'), (3, 'Especializacion'), (4, 'Maestria'), (5, 'Doctorado')])),
            ],
        ),
        migrations.CreateModel(
            name='InstitucionEducativa',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('nombre', models.CharField(max_length=100)),
                ('municipio', models.CharField(max_length=50)),
                ('departamento', models.CharField(max_length=50)),
                ('zona', models.SmallIntegerField(choices=[(0, 'Urbana'), (1, 'Urbana Marginal'), (2, 'Rural'), (3, 'Rural de Difícil Acceso')])),
                ('modalidad', models.SmallIntegerField(choices=[(0, 'Académica'), (1, 'Técnica')])),
                ('orientacion_etnoeducativa', models.SmallIntegerField(choices=[(0, 'Ninguna'), (1, 'Rom'), (2, 'Afrocolombiana'), (3, 'Indígena')])),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_matricula', models.PositiveSmallIntegerField(choices=[(0, 'Matriculado'), (1, 'No Matriculado'), (2, 'En Espera de Matricula')])),
                ('nota_final_curso', models.CharField(max_length=60, default=0)),
                ('identificacion_curso', models.ForeignKey(to='moodle.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=15)),
                ('sexo', models.SmallIntegerField(choices=[(0, 'Masculino'), (1, 'Femenino')])),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.IntegerField()),
                ('fijo', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroNotas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', moodle.models.MinMaxFloat()),
                ('actividad', models.ForeignKey(to='moodle.Actividad')),
                ('cohorte', models.ForeignKey(to='moodle.Cohorte')),
            ],
        ),
        migrations.CreateModel(
            name='SecretariaEducacion',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaderTeacher',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='moodle.Persona')),
                ('grado_estudio', models.CharField(max_length=60)),
            ],
            bases=('moodle.persona',),
        ),
        migrations.CreateModel(
            name='MasterTeacher',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='moodle.Persona')),
                ('tiempo_experiencia', models.CharField(max_length=2)),
                ('cohorte', models.ForeignKey(to='moodle.Cohorte')),
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
            model_name='registronotas',
            name='leader_teacher',
            field=models.ForeignKey(to='moodle.LeaderTeacher'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='identificacion_leader_teacher',
            field=models.ForeignKey(to='moodle.LeaderTeacher'),
        ),
        migrations.AddField(
            model_name='leaderteacher',
            name='institucion',
            field=models.ForeignKey(to='moodle.InstitucionEducativa'),
        ),
    ]
