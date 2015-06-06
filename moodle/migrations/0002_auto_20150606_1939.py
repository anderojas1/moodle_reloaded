# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialacademico',
            name='persona',
        ),
        migrations.RemoveField(
            model_name='historiallaboral',
            name='nivelEscolar',
        ),
        migrations.DeleteModel(
            name='HistorialAcademico',
        ),
        migrations.DeleteModel(
            name='HistorialLaboral',
        ),
        migrations.DeleteModel(
            name='NivelEscolar',
        ),
    ]
