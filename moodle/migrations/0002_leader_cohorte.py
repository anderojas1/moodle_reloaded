# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leader_Cohorte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('cohorte_id', models.ForeignKey(to='moodle.Cohorte')),
                ('leader_id', models.ForeignKey(to='moodle.LeaderTeacher')),
            ],
        ),
    ]
