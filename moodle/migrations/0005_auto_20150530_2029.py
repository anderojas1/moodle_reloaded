# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0004_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohorte',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=60)),
                ('semestre', models.SmallIntegerField(choices=[(0, 'Febrero-Junio'), (1, 'Agosto-Diciembre')])),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='curso',
            field=models.ForeignKey(to='moodle.Curso', default=2),
            preserve_default=False,
        ),
    ]
