# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0013_auto_20160418_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bien',
            name='imagen2',
            field=models.ImageField(blank=True, upload_to='Bien/'),
        ),
        migrations.AlterField(
            model_name='bien',
            name='imagen3',
            field=models.ImageField(blank=True, upload_to='Bien/'),
        ),
        migrations.AlterField(
            model_name='bien',
            name='imagen4',
            field=models.ImageField(blank=True, upload_to='Bien/'),
        ),
        migrations.AlterField(
            model_name='bien',
            name='imagen5',
            field=models.ImageField(blank=True, upload_to='Bien/'),
        ),
    ]
