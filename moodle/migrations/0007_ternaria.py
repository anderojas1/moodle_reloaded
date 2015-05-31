# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0006_actividad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ternaria',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nota', models.FloatField()),
                ('actividad', models.ForeignKey(to='moodle.Actividad')),
                ('cohorte', models.ForeignKey(to='moodle.Cohorte')),
                ('leader_teacher', models.ForeignKey(to='moodle.LeaderTeacher')),
            ],
        ),
    ]
