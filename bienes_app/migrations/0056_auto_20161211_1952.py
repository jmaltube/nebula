# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-11 19:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0055_auto_20161211_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='clasificador',
            name='comision',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='clasificador',
            name='publicidad',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clasificador',
            name='rango',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clasificador',
            name='regalias',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='clasificador',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bienes_app.TipoClasificador'),
        ),
    ]
