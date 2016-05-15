# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 22:03
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    replaces = [('bienes_app', '0017_auto_20160513_1511'), ('bienes_app', '0018_auto_20160513_1550'), ('bienes_app', '0019_auto_20160515_1020'), ('bienes_app', '0020_auto_20160515_1106'), ('bienes_app', '0021_auto_20160515_1118'), ('bienes_app', '0022_remove_cliente_fecha_alta'), ('bienes_app', '0023_cliente_fecha_alta'), ('bienes_app', '0024_auto_20160515_1126'), ('bienes_app', '0025_auto_20160515_1127'), ('bienes_app', '0026_auto_20160515_1145'), ('bienes_app', '0018_auto_20160515_1703'), ('bienes_app', '0019_cliente_rubro'), ('bienes_app', '0020_atributosbien'), ('bienes_app', '0021_auto_20160515_1828'), ('bienes_app', '0022_auto_20160515_1831'), ('bienes_app', '0023_auto_20160515_1839'), ('bienes_app', '0024_auto_20160515_1848'), ('bienes_app', '0025_auto_20160515_1849')]

    dependencies = [
        ('bienes_app', '0016_auto_20160507_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='localidad',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre_fantasia',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='pais',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='partido',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='provincia',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='razon_social',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='bulto',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='plazo_entrega',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='cargo',
            field=models.CharField(choices=[('COM', 'Comprador'), ('VEN', 'Vendedor'), ('COB', 'Cobrador'), ('DIR', 'Director'), ('SOC', 'Socio/Dueño'), ('OTR', 'Otro')], default='OTR', max_length=3),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='celular',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='horario',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Dias y horas de atención'),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='nombre_apellido',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre y apellido'),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='condicion_comercial',
            field=models.CharField(blank=True, choices=[('30F', '30 días F/F'), ('40F', '40 días F/F'), ('60F', '60 días F/F'), ('C40', 'Cheque contra entrega 40 días F/F'), ('CDO', 'Contado'), ('EFT', 'Efectivo'), ('TRF', 'Transferencia')], max_length=3, null=True, verbose_name='Forma de entrega'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='contactos',
            field=models.ManyToManyField(blank=True, to='bienes_app.Contacto'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='cuit',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,11}$', message='No cumple con el formato de CUIT/CUIL')]),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='direccion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RenameField(
            model_name='proveedor',
            old_name='email_oficial',
            new_name='email',
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='fax',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='fecha_incorporacion',
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='forma_entrega',
            field=models.CharField(blank=True, choices=[('REI', 'Se retira en nuestras instalaciones'), ('EEI', 'Se entrega en nuestras instalaciones'), ('RDI', 'Se retira de nuestras instalaciones')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='iva',
            field=models.CharField(blank=True, choices=[('RI', 'Responsable Inscripto'), ('EXC', 'Excento'), ('MON', 'Monotributista'), ('NOR', 'No Responsable')], max_length=3, null=True, verbose_name='Condición frente al IVA'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='localidad',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='nombre_fantasia',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre de fantasía'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='pais',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='partido',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='provincia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tipo',
            field=models.CharField(blank=True, choices=[('BIU', 'Bien de uso'), ('GVA', 'Gastos varios'), ('IMP', 'Impuesto'), ('INS', 'Insumo'), ('MPR', 'Materia prima'), ('PTE', 'Producto terminado'), ('SVC', 'Servicio'), ('SBP', 'Subproducto')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tipo_factura',
            field=models.CharField(blank=True, choices=[('FTA', 'Factura A'), ('FTB', 'Factura B'), ('FTA', 'Factura A'), ('FTC', 'Factura C'), ('FTE', 'Factura E'), ('FTM', 'Factura M'), ('NCA', 'Nota de crédito A'), ('NCB', 'Nota de crédito B'), ('NCC', 'Nota de crédito C'), ('NCE', 'Nota de crédito E'), ('NCM', 'Nota de crédito M'), ('NDA', 'Nota de débito A'), ('NDB', 'Nota de débito B'), ('NDC', 'Nota de débito C'), ('NDE', 'Nota de débito E'), ('NDM', 'Nota de débito M')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='dto1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='dto2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='compra',
            name='dto3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
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
        migrations.AddField(
            model_name='cliente',
            name='agente_perc_iibb',
            field=models.BooleanField(default=False, verbose_name='Agente percepcion de IIBB'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='agente_perc_iigg',
            field=models.BooleanField(default=False, verbose_name='Agente percepcion de IIGG'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='agente_perc_iva',
            field=models.BooleanField(default=False, verbose_name='Agente percepcion de IVA'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='agente_perc_ss',
            field=models.BooleanField(default=False, verbose_name='Agente percepcion de seguridad social'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='alerta',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='comprobante_cuit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='condicion_comercial',
            field=models.CharField(blank=True, choices=[('30F', '30 días F/F'), ('40F', '40 días F/F'), ('60F', '60 días F/F'), ('C40', 'Cheque contra entrega 40 días F/F'), ('CDO', 'Contado'), ('EFT', 'Efectivo'), ('TRF', 'Transferencia')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='corredor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Proveedor'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cuit',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,11}$', message='No cumple con el formato de CUIT/CUIL')]),
        ),
        migrations.AddField(
            model_name='cliente',
            name='expreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bienes_app.Expreso'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='forma_entrega',
            field=models.CharField(blank=True, choices=[('REI', 'Se retira en nuestras instalaciones'), ('EEI', 'Se entrega en nuestras instalaciones'), ('RDI', 'Se retira de nuestras instalaciones')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='informe_economico',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='iva',
            field=models.CharField(blank=True, choices=[('RI', 'Responsable Inscripto'), ('EXC', 'Excento'), ('MON', 'Monotributista'), ('NOR', 'No Responsable')], max_length=3, null=True, verbose_name='Condición frente al IVA'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='jurisdiccion_iibb',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='limite_credito',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Límite de crédito'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='mayorista',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cliente',
            name='tipo_factura',
            field=models.CharField(blank=True, choices=[('FTA', 'Factura A'), ('FTB', 'Factura B'), ('FTA', 'Factura A'), ('FTC', 'Factura C'), ('FTE', 'Factura E'), ('FTM', 'Factura M'), ('NCA', 'Nota de crédito A'), ('NCB', 'Nota de crédito B'), ('NCC', 'Nota de crédito C'), ('NCE', 'Nota de crédito E'), ('NCM', 'Nota de crédito M'), ('NDA', 'Nota de débito A'), ('NDB', 'Nota de débito B'), ('NDC', 'Nota de débito C'), ('NDE', 'Nota de débito E'), ('NDM', 'Nota de débito M')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='condicion_comercial',
            field=models.CharField(blank=True, choices=[('30F', '30 días F/F'), ('40F', '40 días F/F'), ('60F', '60 días F/F'), ('C40', 'Cheque contra entrega 40 días F/F'), ('CDO', 'Contado'), ('EFT', 'Efectivo'), ('TRF', 'Transferencia')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='forma_entrega',
            field=models.CharField(blank=True, choices=[('REI', 'Se retira en nuestras instalaciones'), ('EEI', 'Se entrega en nuestras instalaciones'), ('RDI', 'Se retira de nuestras instalaciones')], max_length=3, null=True, verbose_name='Forma de entrega'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 5, 15, 14, 18, 28, 441539, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_alta',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='real',
        ),
        migrations.AddField(
            model_name='proveedor',
            name='corredor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='compra',
            name='ultima_fecha',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterModelOptions(
            name='compra',
            options={'verbose_name': 'Costo de proveedor', 'verbose_name_plural': 'Costos de proveedores'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'ordering': ['razon_social', 'nombre_fantasia'], 'verbose_name_plural': 'Proveedores'},
        ),
        migrations.AlterField(
            model_name='cliente',
            name='razon_social',
            field=models.CharField(default='razon social prueba', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='rubro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bienes_app.Rubro'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Atributo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('titulo',),
                'verbose_name_plural': 'Atributos',
            },
        ),
        migrations.CreateModel(
            name='AtributosBien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=9000)),
                ('atributo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bienes_app.Atributo')),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bienes_app.Bien')),
            ],
        ),
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
        migrations.DeleteModel(
            name='AtributosBien',
        ),
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
