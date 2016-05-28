# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0024_auto_20160515_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='BienYAtributo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=9000)),
                ('atributo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bienes_app.Atributo')),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bienes_app.Bien')),
            ],
        ),
        migrations.AddField(
            model_name='bien',
            name='atributos',
            field=models.ManyToManyField(through='bienes_app.BienYAtributo', to='bienes_app.Atributo'),
        ),
        migrations.AlterUniqueTogether(
            name='bienyatributo',
            unique_together=set([('bien', 'atributo')]),
        ),
    ]