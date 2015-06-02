# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moodle', '0003_master_cohorte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master_cohorte',
            name='cohorte_id',
        ),
        migrations.RemoveField(
            model_name='master_cohorte',
            name='master_id',
        ),
        migrations.DeleteModel(
            name='Master_Cohorte',
        ),
    ]
