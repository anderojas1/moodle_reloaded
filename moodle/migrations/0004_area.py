# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0003_curso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.CharField(serialize=False, max_length=60, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField(max_length=200)),
            ],
        ),
    ]
