# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0008_auto_20150604_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialLaboral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='NivelEscolar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.SmallIntegerField(max_length=100, choices=[(0, 'Transicion'), (1, 'Educacion Inicial'), (2, 'Educacion basica primaria'), (3, 'Educacion basica secundaria'), (4, 'Educacion media'), (5, 'Nivel Superior')])),
                ('soporte', models.FileField(upload_to='Documentos_Soporte')),
            ],
        ),
        migrations.RemoveField(
            model_name='nivelesacademicos',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='historialacademico',
            name='leader',
        ),
        migrations.AddField(
            model_name='historialacademico',
            name='persona',
            field=models.ForeignKey(null=True, to='moodle.Persona'),
        ),
        migrations.DeleteModel(
            name='NivelesAcademicos',
        ),
        migrations.AddField(
            model_name='historiallaboral',
            name='nivelEscolar',
            field=models.ForeignKey(to='moodle.NivelEscolar'),
        ),
    ]
