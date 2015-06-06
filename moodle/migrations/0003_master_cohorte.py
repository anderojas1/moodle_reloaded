# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0002_leader_cohorte'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master_Cohorte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cohorte_id', models.ForeignKey(to='moodle.Cohorte')),
                ('master_id', models.ForeignKey(to='moodle.MasterTeacher')),
            ],
        ),
    ]
