# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171209_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
    ]