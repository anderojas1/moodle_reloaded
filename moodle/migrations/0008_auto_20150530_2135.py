# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import moodle.models


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0007_ternaria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ternaria',
            name='nota',
            field=moodle.models.MinMaxFloat(),
        ),
    ]
