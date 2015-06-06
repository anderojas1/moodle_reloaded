# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0007_nivelesacademicos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nivelesacademicos',
            name='leader',
            field=models.OneToOneField(to='moodle.LeaderTeacher'),
        ),
    ]
