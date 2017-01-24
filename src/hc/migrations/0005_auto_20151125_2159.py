# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc', '0004_auto_20151122_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newentry',
            name='last_updated_by',
            field=models.CharField(default='reception', max_length=15, blank=True),
            preserve_default=False,
        ),
    ]
