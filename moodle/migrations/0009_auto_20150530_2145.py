# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import moodle.models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0008_auto_20150530_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroNotas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nota', moodle.models.MinMaxFloat()),
                ('actividad', models.ForeignKey(to='moodle.Actividad')),
                ('cohorte', models.ForeignKey(to='moodle.Cohorte')),
                ('leader_teacher', models.ForeignKey(to='moodle.LeaderTeacher')),
            ],
        ),
        migrations.RemoveField(
            model_name='ternaria',
            name='actividad',
        ),
        migrations.RemoveField(
            model_name='ternaria',
            name='cohorte',
        ),
        migrations.RemoveField(
            model_name='ternaria',
            name='leader_teacher',
        ),
        migrations.DeleteModel(
            name='Ternaria',
        ),
    ]
