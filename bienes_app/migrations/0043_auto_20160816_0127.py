# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-16 01:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0042_auto_20160816_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proformaybien',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bienes_app.PedidoYBien'),
        ),
        migrations.AlterUniqueTogether(
            name='proformaybien',
            unique_together=set([('proforma', 'item')]),
        ),
    ]
