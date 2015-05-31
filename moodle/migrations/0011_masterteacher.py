# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0010_matricula'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterTeacher',
            fields=[
                ('persona_ptr', models.OneToOneField(serialize=False, primary_key=True, to='moodle.Persona', parent_link=True, auto_created=True)),
                ('tiempo_experiencia', models.CharField(max_length=2)),
                ('cohorte', models.ForeignKey(to='moodle.Cohorte')),
            ],
            bases=('moodle.persona',),
        ),
    ]
