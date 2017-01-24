# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='diary_valid_through',
            field=models.DateField(default=datetime.datetime(2016, 6, 30, 0, 0), verbose_name=b'Valid through'),
        ),
    ]
