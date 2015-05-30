# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0005_auto_20150530_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.CharField(max_length=60, serialize=False, primary_key=True)),
                ('descripcion', models.TextField(max_length=200)),
                ('titulo', models.CharField(max_length=60)),
                ('fecha_fin', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('porcentaje', models.CharField(max_length=60)),
            ],
        ),
    ]
