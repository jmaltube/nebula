# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-12 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0067_auto_20161212_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='nombre_fantasia',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='razon_social',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombre_fantasia',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre de fantasía'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='razon_social',
            field=models.CharField(max_length=200),
        ),
    ]