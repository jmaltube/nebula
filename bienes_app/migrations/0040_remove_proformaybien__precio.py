# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-14 22:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0039_proformaybien__precio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proformaybien',
            name='_precio',
        ),
    ]