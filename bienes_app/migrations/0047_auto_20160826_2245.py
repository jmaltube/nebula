# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-26 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0046_auto_20160826_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='cerrado',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='confirmado_x_cliente',
            field=models.BooleanField(default=True),
        ),
    ]
