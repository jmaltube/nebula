# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-26 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0045_auto_20160824_1740'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedidoybien',
            options={'verbose_name_plural': ' Pedidos (items pendientes)'},
        ),
        migrations.AlterField(
            model_name='cliente',
            name='habilitado',
            field=models.BooleanField(default=False, help_text='Editable solo por admin'),
        ),
    ]
