# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0006_historialacademico_leader'),
    ]

    operations = [
        migrations.CreateModel(
            name='NivelesAcademicos',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('choice_fiels', models.CharField(verbose_name='Algunas Elecciones ..', choices=[(0, 'julian'), (1, 'anderson')], max_length=50)),
                ('leader', models.ForeignKey(unique=True, to='moodle.LeaderTeacher')),
            ],
        ),
    ]
