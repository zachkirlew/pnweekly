# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20171209_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='model_pic',
            field=models.ImageField(blank=True, upload_to='user_images/'),
        ),
    ]
