# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-13 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bienes_app', '0032_auto_20160706_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda', models.CharField(choices=[('ARS', 'Peso Argentino'), ('USD', 'Dólar'), ('EUR', 'Euro'), ('BRL', 'Real')], max_length=3, unique=True)),
                ('cotizacion', models.DecimalField(decimal_places=2, max_digits=5)),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='bien',
            options={'ordering': ['codigo', 'denominacion'], 'permissions': (('action_bien', 'Ejecutar acciones'),), 'verbose_name_plural': ' Bienes'},
        ),
        migrations.AlterModelOptions(
            name='cliente',
            options={'verbose_name_plural': ' Clientes'},
        ),
        migrations.AlterModelOptions(
            name='lista',
            options={'ordering': ['tipo', 'nombre'], 'permissions': (('action_lista', 'Ejecutar acciones'),), 'verbose_name_plural': ' Listas'},
        ),
        migrations.AlterModelOptions(
            name='pedido',
            options={'permissions': (('action_pedido', 'Ejecutar acciones'),), 'verbose_name_plural': ' Pedidos'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'ordering': ['razon_social', 'nombre_fantasia'], 'verbose_name_plural': ' Proveedores'},
        ),
        migrations.AlterField(
            model_name='compra',
            name='moneda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Moneda'),
        ),
        migrations.AlterField(
            model_name='lista',
            name='moneda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Moneda'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_actualizacion',
            field=models.DateField(auto_now=True, verbose_name='Ult. modificación'),
        ),
    ]
