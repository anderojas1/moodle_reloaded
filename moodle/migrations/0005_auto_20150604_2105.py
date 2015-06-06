# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0004_auto_20150602_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialacademico',
            name='fecha_realizacion',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historialacademico',
            name='institucionAcre',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='historialacademico',
            name='titulo',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
    ]
