# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 14:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0021_auto_20160515_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='fecha_alta',
        ),
    ]
