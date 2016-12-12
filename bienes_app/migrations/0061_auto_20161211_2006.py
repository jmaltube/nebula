# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-11 20:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0060_auto_20161211_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='bien',
            name='e',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bien',
            name='primeros_4_digitos',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999, message='Hasta 4 digitos.')]),
        ),
        migrations.AddField(
            model_name='bien',
            name='r',
            field=models.BooleanField(default=False),
        ),
    ]