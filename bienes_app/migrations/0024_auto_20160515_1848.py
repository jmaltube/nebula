# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 21:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0023_auto_20160515_1839'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='atributosbien',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='atributosbien',
            name='atributo',
        ),
        migrations.RemoveField(
            model_name='atributosbien',
            name='bien',
        ),
        migrations.RemoveField(
            model_name='bien',
            name='atributos',
        ),
        migrations.DeleteModel(
            name='AtributosBien',
        ),
    ]
