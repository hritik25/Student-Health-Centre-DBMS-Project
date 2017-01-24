# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import hc.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='newEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_time', models.DateTimeField(auto_now_add=True, verbose_name=b'Time of Entry')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name=b'Record updated at')),
                ('stay_day', models.SmallIntegerField(verbose_name=b'Stay Duration (Days)', validators=[django.core.validators.MaxValueValidator(15), django.core.validators.MinValueValidator(1)])),
                ('stay_cause', models.CharField(max_length=30, null=True, verbose_name=b'Cause of stay')),
                ('stay_bed', models.SmallIntegerField(verbose_name=b'Bed No.', validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(1)])),
                ('blood_test_report', models.FileField(null=True, upload_to=hc.models.blood_report_path)),
                ('xray_report', models.FileField(null=True, upload_to=hc.models.xray_path)),
                ('last_updated_by', models.CharField(max_length=15, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('roll_no', models.CharField(max_length=10, serialize=False, verbose_name=b'Student ID No.', primary_key=True)),
                ('full_name', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('faculty', models.CharField(max_length=3, choices=[(b'CSE', b'Computer Science'), (b'EC', b'Electronics Engineerning'), (b'MEC', b'Mechanical Engineering'), (b'CER', b'Ceramic Engineering'), (b'CIV', b'Civil Engineering'), (b'EL', b'Electrical Engineering'), (b'MnC', b'Maths and Computing')])),
                ('year', models.CharField(max_length=2, choices=[(b'1', b'First Year'), (b'2', b'Second Year'), (b'3', b'Third Year'), (b'4', b'Fourth Year'), (b'5', b'IDD/IMD Fifth Year'), (b'M1', b'MTech First Year'), (b'M2', b'MTech Second Year'), (b'P', b'PHD')])),
                ('DOB', models.DateField(verbose_name=b'Date of birth')),
                ('blood_group', models.CharField(max_length=3, choices=[(b'A+', b'A+'), (b'B+', b'B+'), (b'O+', b'O+'), (b'AB+', b'AB+'), (b'A-', b'A-'), (b'B-', b'B-'), (b'O-', b'O-'), (b'AB-', b'AB-')])),
                ('diary_issue_date', models.DateField(auto_now=True, verbose_name=b'Date of issue')),
                ('diary_valid_through', models.DateField(default=datetime.datetime(2015, 6, 30, 0, 0), verbose_name=b'Valid through')),
                ('phone_number', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{10,10}$', message=b'Phone number must be a valid 10 digit number.')])),
            ],
        ),
        migrations.AddField(
            model_name='newentry',
            name='student_id',
            field=models.ForeignKey(to='hc.Student'),
        ),
    ]
