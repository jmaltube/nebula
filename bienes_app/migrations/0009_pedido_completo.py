# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0008_auto_20160407_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='completo',
            field=models.BooleanField(default=False),
        ),
    ]
