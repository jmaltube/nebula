# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0003_auto_20160402_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='lista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Lista'),
        ),
    ]