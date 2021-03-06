# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-12 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0065_auto_20161212_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cuit',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='iva',
            field=models.CharField(blank=True, choices=[('RI', 'Responsable Inscripto'), ('EXC', 'Excento'), ('MON', 'Monotributista'), ('NOR', 'No Responsable'), ('CF', 'Consumidor Final')], max_length=3, null=True, verbose_name='Condición frente al IVA'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='iva',
            field=models.CharField(blank=True, choices=[('RI', 'Responsable Inscripto'), ('EXC', 'Excento'), ('MON', 'Monotributista'), ('NOR', 'No Responsable'), ('CF', 'Consumidor Final')], max_length=3, null=True, verbose_name='Condición frente al IVA'),
        ),
    ]
