# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-16 23:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0034_pedidoybien_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidoybien',
            old_name='cantidad',
            new_name='cantidad_solicitada',
        ),
        migrations.RemoveField(
            model_name='pedidoybien',
            name='entregado',
        ),
        migrations.AddField(
            model_name='pedidoybien',
            name='cantidad_entregada',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, message='Solo cantidades positivas.')]),
        ),
        migrations.AlterField(
            model_name='pedidoybien',
            name='precio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]