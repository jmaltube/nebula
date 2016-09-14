# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-01 03:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0048_auto_20160829_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proformaybien',
            name='cantidad',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Solo cantidades positivas.')]),
        ),
    ]
