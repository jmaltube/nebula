# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-12 01:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0064_auto_20161212_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bienes_app.TipoClasificador'),
        ),
    ]