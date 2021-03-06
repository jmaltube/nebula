# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 14:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0025_auto_20160515_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='real',
        ),
        migrations.AddField(
            model_name='proveedor',
            name='corredor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='corredor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Proveedor'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='expreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Expreso'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 5, 15, 14, 45, 52, 665098, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='compra',
            name='ultima_fecha',
            field=models.DateField(auto_now=True),
        ),
    ]
