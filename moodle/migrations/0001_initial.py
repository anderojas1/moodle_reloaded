# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import moodle.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('descripcion', models.TextField(max_length=200)),
                ('titulo', models.CharField(max_length=60)),
                ('fecha_fin', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('porcentaje', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='ActividadesCohorte',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('actividad', models.ForeignKey(to='moodle.Actividad')),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=60)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cohorte',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=60)),
                ('semestre', models.SmallIntegerField(blank=True, choices=[(0, 'Febrero-Junio'), (1, 'Agosto-Diciembre')], null=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=60)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
                ('estado', models.BooleanField(default=True)),
                ('area', models.ForeignKey(to='moodle.Area')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialAcademico',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('titulo', models.CharField(max_length=60)),
                ('tipoEstudio', models.SmallIntegerField(choices=[(0, 'Bachillerato'), (1, 'Pregrado'), (2, 'Posgrado'), (3, 'Especializacion'), (4, 'Maestria'), (5, 'Doctorado')])),
                ('fechaRealizacion', models.DateField()),
                ('institucionAcree', models.CharField(max_length=100)),
                ('evidencia', models.FileField(upload_to='Documentos_soporte')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialLaboral',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tiempoLaborado', models.CharField(max_length=2)),
                ('nivelesEscolares', models.TextField(max_length=300)),
                ('areasDesempenio', models.TextField(max_length=300)),
                ('gradosLaborales', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='InstitucionEducativa',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=10)),
                ('nombre', models.CharField(max_length=100)),
                ('municipio', models.CharField(max_length=50)),
                ('departamento', models.CharField(max_length=50)),
                ('zona', models.SmallIntegerField(choices=[(0, 'Urbana'), (1, 'Urbana Marginal'), (2, 'Rural'), (3, 'Rural de Difícil Acceso')])),
                ('modalidad', models.SmallIntegerField(choices=[(0, 'Académica'), (1, 'Técnica')])),
                ('orientacion_etnoeducativa', models.SmallIntegerField(choices=[(0, 'Ninguna'), (1, 'Rom'), (2, 'Afrocolombiana'), (3, 'Indígena')])),
            ],
        ),
        migrations.CreateModel(
            name='Leader_Cohorte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cohorte_id', models.ForeignKey(to='moodle.Cohorte')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('estado_matricula', models.PositiveSmallIntegerField(choices=[(0, 'Matriculado'), (1, 'No Matriculado'), (2, 'En Espera de Matricula')])),
                ('nota_final_curso', models.CharField(default=0, max_length=60)),
                ('identificacion_curso', models.ForeignKey(to='moodle.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=15)),
                ('sexo', models.SmallIntegerField(choices=[(0, 'Masculino'), (1, 'Femenino')])),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.BigIntegerField()),
                ('fijo', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroNotas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nota', moodle.models.MinMaxFloat()),
                ('actividad', models.ForeignKey(to='moodle.Actividad')),
                ('cohorte', models.ForeignKey(to='moodle.Cohorte')),
            ],
        ),
        migrations.CreateModel(
            name='SecretariaEducacion',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoporteLaboralNuevo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tiempo', models.CharField(max_length=2)),
                ('nombreInsti', models.CharField(max_length=60)),
                ('docSoporte', models.FileField(upload_to='DocumentosSoporte')),
            ],
        ),
        migrations.CreateModel(
            name='DatosDemograficos',
            fields=[
                ('id', models.OneToOneField(to='moodle.Persona', serialize=False, primary_key=True)),
                ('estrato', moodle.models.MinMaxFloat()),
                ('tipo_vivienda', models.PositiveSmallIntegerField(choices=[(0, 'Apartaestudio'), (1, 'Apartamento'), (2, 'Casa')])),
                ('caracter_vivienda', models.PositiveSmallIntegerField(choices=[(0, 'Arrendada'), (1, 'Familiar'), (2, 'Propia')])),
                ('personas_convive', models.CharField(max_length=2)),
                ('estado_civil', models.PositiveSmallIntegerField(choices=[(0, 'Viudo'), (1, 'Soltero'), (2, 'Divorciado'), (3, 'Union Libre'), (4, 'Casado')])),
                ('numero_hijos', models.CharField(max_length=2)),
                ('ciudad_nacimiento', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='LeaderTeacher',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='moodle.Persona', serialize=False, primary_key=True)),
                ('grado_estudio', models.CharField(max_length=60)),
            ],
            bases=('moodle.persona',),
        ),
        migrations.CreateModel(
            name='MasterTeacher',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='moodle.Persona', serialize=False, primary_key=True)),
                ('tiempo_experiencia', models.CharField(max_length=2)),
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
            model_name='historiallaboral',
            name='persona',
            field=models.OneToOneField(to='moodle.Persona'),
        ),
        migrations.AddField(
            model_name='historiallaboral',
            name='soporteLaboral',
            field=models.ManyToManyField(to='moodle.SoporteLaboralNuevo'),
        ),
        migrations.AddField(
            model_name='historialacademico',
            name='persona',
            field=models.OneToOneField(to='moodle.Persona'),
        ),
        migrations.AddField(
            model_name='cohorte',
            name='curso',
            field=models.ForeignKey(to='moodle.Curso'),
        ),
        migrations.AddField(
            model_name='actividadescohorte',
            name='cohorte',
            field=models.ForeignKey(to='moodle.Cohorte'),
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
        migrations.AddField(
            model_name='leader_cohorte',
            name='leader_id',
            field=models.ForeignKey(to='moodle.LeaderTeacher'),
        ),
        migrations.AddField(
            model_name='cohorte',
            name='master',
            field=models.ForeignKey(blank=True, to='moodle.MasterTeacher', null=True),
        ),
    ]
