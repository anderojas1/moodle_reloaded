# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0005_auto_20150604_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialacademico',
            name='leader',
            field=models.ForeignKey(null=True, to='moodle.LeaderTeacher'),
        ),
    ]
