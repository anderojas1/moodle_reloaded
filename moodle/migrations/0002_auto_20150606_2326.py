# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cohorte',
            name='fecha_fin',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='cohorte',
            name='fecha_inicio',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='cohorte',
            name='master',
            field=models.ForeignKey(to='moodle.MasterTeacher', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cohorte',
            name='semestre',
            field=models.SmallIntegerField(null=True, choices=[(0, 'Febrero-Junio'), (1, 'Agosto-Diciembre')]),
        ),
        migrations.AlterField(
            model_name='persona',
            name='celular',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='persona',
            name='fijo',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]
