# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alertpreference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertpreference',
            name='user',
        ),
        migrations.AddField(
            model_name='customuser',
            name='business',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='music',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='sport',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='technology',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.DeleteModel(
            name='AlertPreference',
        ),
    ]
