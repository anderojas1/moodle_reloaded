# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0009_auto_20150605_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nivelescolar',
            name='nombre',
            field=models.SmallIntegerField(choices=[(0, 'Transicion'), (1, 'Educacion Inicial'), (2, 'Educacion basica primaria'), (3, 'Educacion basica secundaria'), (4, 'Educacion media'), (5, 'Nivel Superior')]),
        ),
    ]
