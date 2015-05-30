# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0011_masterteacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialAcademico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('tipoEstudio', models.PositiveSmallIntegerField(choices=[(0, 'Bachillerato'), (1, 'Pregrado'), (2, 'Posgrado'), (3, 'Especializacion'), (4, 'Maestria'), (5, 'Doctorado')])),
            ],
        ),
        migrations.AddField(
            model_name='leaderteacher',
            name='grado_estudio',
            field=models.CharField(max_length=60, default=1),
            preserve_default=False,
        ),
    ]
