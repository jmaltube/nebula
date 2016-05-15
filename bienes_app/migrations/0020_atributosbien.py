# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 21:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0019_cliente_rubro'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtributosBien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('texto', models.TextField(max_length=9000)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bienes_app.Bien')),
            ],
        ),
    ]
