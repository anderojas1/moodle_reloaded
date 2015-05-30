# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0002_auto_20150530_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=60, serialize=False)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
            ],
        ),
    ]
