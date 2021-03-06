# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 13:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0018_auto_20160513_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacion', models.CharField(max_length=50)),
                ('direccion', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='email oficial'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 5, 15, 13, 20, 4, 623252, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='teléfono oficial'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_actualizacion',
            field=models.DateField(auto_now=True),
        ),
    ]
