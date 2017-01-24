# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hc', '0003_auto_20151122_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newentry',
            name='stay_bed',
            field=models.SmallIntegerField(null=True, verbose_name=b'Bed No.', validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='newentry',
            name='stay_day',
            field=models.SmallIntegerField(null=True, verbose_name=b'Stay Duration (Days)', validators=[django.core.validators.MaxValueValidator(15), django.core.validators.MinValueValidator(1)]),
        ),
    ]
