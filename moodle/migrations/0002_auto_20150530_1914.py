# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institucioneducativa',
            name='modalidad',
            field=models.SmallIntegerField(choices=[(0, 'Académica'), (1, 'Técnica')]),
        ),
        migrations.AlterField(
            model_name='institucioneducativa',
            name='orientacion_etnoeducativa',
            field=models.SmallIntegerField(choices=[(0, 'Ninguna'), (1, 'Rom'), (2, 'Afrocolombiana'), (3, 'Indígena')]),
        ),
        migrations.AlterField(
            model_name='institucioneducativa',
            name='zona',
            field=models.SmallIntegerField(choices=[(0, 'Urbana'), (1, 'Urbana Marginal'), (2, 'Rural'), (3, 'Rural de Difícil Acceso')]),
        ),
        migrations.AlterField(
            model_name='persona',
            name='sexo',
            field=models.SmallIntegerField(choices=[(0, 'Masculino'), (1, 'Femenino')]),
        ),
    ]
