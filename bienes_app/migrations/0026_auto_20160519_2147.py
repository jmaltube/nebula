# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-20 00:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0025_auto_20160515_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compra',
            options={'permissions': (('action_proveedor', 'Ejecutar acciones'),), 'verbose_name': 'Costo de proveedor', 'verbose_name_plural': 'Costos de proveedores'},
        ),
        migrations.AddField(
            model_name='bien',
            name='tags',
            field=models.CharField(default='Industrial Resistente', max_length=100),
            preserve_default=False,
        ),
    ]