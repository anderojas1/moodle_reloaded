# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0009_auto_20150530_2145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('estado_matricula', models.PositiveSmallIntegerField(choices=[(0, 'Matriculado'), (1, 'No Matriculado'), (2, 'En Espera de Matricula')])),
                ('nota_final_curso', models.CharField(max_length=60, default=0)),
                ('identificacion_curso', models.ForeignKey(to='moodle.Curso')),
                ('identificacion_leader_teacher', models.ForeignKey(to='moodle.LeaderTeacher')),
            ],
        ),
    ]
