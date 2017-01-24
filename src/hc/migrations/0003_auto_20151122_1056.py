# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hc', '0002_auto_20151114_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.CharField(max_length=10, choices=[(b'1st', b'First Year'), (b'2nd', b'Second Year'), (b'3rd', b'Third Year'), (b'4th', b'Fourth Year'), (b'5th', b'IDD/IMD Fifth Year'), (b'M.Tech 1st', b'MTech First Year'), (b'M.Tech 2nd', b'MTech Second Year'), (b'PHD', b'PHD')]),
        ),
    ]
