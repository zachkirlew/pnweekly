# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-13 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20171213_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='model_pic',
            field=models.ImageField(default='user_images/no-image.jpg', upload_to=users.models.CustomUser.path_and_rename),
        ),
    ]
