# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0004_datosdemograficos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosdemograficos',
            name='id',
            field=models.OneToOneField(primary_key=True, to='moodle.Persona', serialize=False),
        ),
    ]
