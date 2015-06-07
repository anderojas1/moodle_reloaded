# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import moodle.models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0003_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosDemograficos',
            fields=[
                ('id', models.ForeignKey(serialize=False, to='moodle.Persona', primary_key=True)),
                ('estrato', moodle.models.MinMaxFloat()),
                ('tipo_vivienda', models.PositiveSmallIntegerField(choices=[(0, 'Apartaestudio'), (1, 'Apartamento'), (2, 'Casa')])),
                ('caracter_vivienda', models.PositiveSmallIntegerField(choices=[(0, 'Arrendada'), (1, 'Familiar'), (2, 'Propia')])),
                ('personas_convive', models.CharField(max_length=2)),
                ('estado_civil', models.PositiveSmallIntegerField(choices=[(0, 'Viudo'), (1, 'Soltero'), (2, 'Divorciado'), (3, 'Union Libre'), (4, 'Casado')])),
                ('numero_hijos', models.CharField(max_length=2)),
                ('ciudad_nacimiento', models.CharField(max_length=20)),
            ],
        ),
    ]
