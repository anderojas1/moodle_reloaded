# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0005_auto_20150607_0329'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialAcademico',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('titulo', models.CharField(max_length=60)),
                ('tipoEstudio', models.SmallIntegerField(choices=[(0, 'Bachillerato'), (1, 'Pregrado'), (2, 'Posgrado'), (3, 'Especializacion'), (4, 'Maestria'), (5, 'Doctorado')])),
                ('fechaRealizacion', models.DateField()),
                ('institucionAcree', models.CharField(max_length=100)),
                ('evidencia', models.FileField(upload_to='Documentos_soporte')),
                ('persona', models.OneToOneField(to='moodle.Persona')),
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
                ('persona', models.OneToOneField(to='moodle.Persona')),
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
        migrations.AlterField(
            model_name='cohorte',
            name='fecha_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cohorte',
            name='fecha_inicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cohorte',
            name='semestre',
            field=models.SmallIntegerField(blank=True, null=True, choices=[(0, 'Febrero-Junio'), (1, 'Agosto-Diciembre')]),
        ),
        migrations.AddField(
            model_name='historiallaboral',
            name='soporteLaboral',
            field=models.ManyToManyField(to='moodle.SoporteLaboralNuevo'),
        ),
    ]
