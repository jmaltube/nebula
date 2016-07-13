# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.signing import Signer
import operator

IVA = [('RI','Responsable Inscripto'), ('EXC','Excento'), ('MON', 'Monotributista'), ('NOR', 'No Responsable')]

CondicionComercial = [('30F','30 días F/F'), ('40F','40 días F/F'),('60F', '60 días F/F'),
        ('C40', 'Cheque contra entrega 40 días F/F'),('CDO', 'Contado'),('EFT', 'Efectivo'),
        ('TRF', 'Transferencia')
        ]         

FormaEntrega = [('REI','Se retira en nuestras instalaciones'),
        ('EEI','Se entrega en nuestras instalaciones'),
        ('RDI', 'Se retira de nuestras instalaciones')                                           
        ]         

TipoFactura = [('FTA','Factura A'), ('FTB','Factura B'),('FTA','Factura A'),
        ('FTC','Factura C'),('FTE','Factura E'),('FTM','Factura M'),
        ('NCA','Nota de crédito A'),('NCB','Nota de crédito B'),('NCC','Nota de crédito C'),
        ('NCE','Nota de crédito E'),('NCM','Nota de crédito M'),('NDA','Nota de débito A'),
        ('NDB','Nota de débito B'),('NDC','Nota de débito C'),('NDE','Nota de débito E'),
        ('NDM','Nota de débito M')                                               
        ]   

Moneda = [('ARS','Peso Argentino'),('USD','Dólar'),('EUR','Euro'), ('BRL', 'Real')]


class Moneda(models.Model):
    moneda = models.CharField(choices=Moneda, max_length=3, unique=True)
    cotizacion = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return u"%s (%s)" %(self.moneda, self.cotizacion)
    
    def __unicode__(self):
        return u"%s (%s)" %(self.moneda, self.cotizacion)
    


class Abastecimiento(models.Model):
    denominacion = models.CharField(max_length=50) 

    def __str__(self):
        return self.denominacion
    
    class Meta:
        ordering = ["denominacion"]
        verbose_name = "Forma de Abastecimiento"
        verbose_name_plural = "Formas de Abastecimiento"

class Marca(models.Model):
    denominacion = models.CharField(max_length=50) 

    def __str__(self):
        return self.denominacion
    
    class Meta:
        ordering = ["denominacion"]                

class Rubro(models.Model):
    denominacion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.denominacion    
        
    class Meta:
        ordering = ["denominacion"]
        verbose_name_plural = "Rubros"
                 
class Clasificador(models.Model):
    denominacion = models.CharField(max_length=50)
    rubro = models.ForeignKey(Rubro)
    
    def __str__(self):
        return self.denominacion + " | " + self.rubro.denominacion 

    def __unicode__(self):
        return self.denominacion + " | " + self.rubro.denominacion 

    class Meta:
        ordering = ["denominacion"]
        verbose_name_plural = "Clasificadores"

class Impuesto(models.Model):
    impuesto = models.CharField(max_length=20, unique=True)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return "{0}: {1}%".format(self.impuesto, self.valor)
    
    def __unicode__(self):
        return "{0}: {1}%".format(self.impuesto, self.valor)
    
class Contacto(models.Model):
    Cargo = [('COM','Comprador'), ('VEN','Vendedor'), ('COB', 'Cobrador'),
            ('DIR', 'Director'), ('SOC', 'Socio/Dueño'),('OTR', 'Otro')
            ]
            
    nombre_apellido = models.CharField(verbose_name="Nombre y apellido",max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=3, choices=Cargo, default='OTR')
    telefono = models.CharField(max_length=50,blank=True, null=True)
    celular = models.CharField(max_length=50,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    horario = models.CharField(verbose_name="Dias y horas de atención",max_length=50,blank=True, null=True)
    
    def __str__(self):
        return self.nombre_apellido
        
    class Meta:
        ordering = ["nombre_apellido"]
        verbose_name_plural = "Contactos"


class Proveedor(models.Model):
            
    TipoProveedor = [('BIU','Bien de uso'), ('GVA','Gastos varios'), ('IMP', 'Impuesto'),
            ('INS', 'Insumo'), ('MPR', 'Materia prima'), ('PTE', 'Producto terminado'),
            ('SVC', 'Servicio'), ('SBP', 'Subproducto')                    
            ]         

    #Datos generales
    razon_social = models.CharField(max_length=50)
    nombre_fantasia = models.CharField(verbose_name='Nombre de fantasía',max_length=50,blank=True, null=True)
    fecha_alta = models.DateField(auto_now_add=True)
    habilitado = models.BooleanField(default=True)
    telefono = models.CharField(max_length=50,blank=True, null=True)
    fax = models.CharField(max_length=50,blank=True, null=True)
    website = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tipo = models.CharField(max_length=3, choices=TipoProveedor,blank=True, null=True)
    direccion = models.CharField(max_length=100,blank=True, null=True)
    codigo_postal = models.CharField(max_length=10,blank=True, null=True)
    partido = models.CharField(max_length=100,blank=True, null=True)
    localidad = models.CharField(max_length=100,blank=True, null=True)
    provincia = models.CharField(max_length=100,blank=True, null=True)
    pais = models.CharField(max_length=100,blank=True, null=True)
    contactos = models.ManyToManyField(Contacto,blank=True)    
    
    #Datos comerciales
    cuit = models.CharField(max_length=11, blank=True, null=True, validators=[RegexValidator(r'^\d{1,11}$',message="No cumple con el formato de CUIT/CUIL")])    
    condicion_comercial = models.CharField(max_length=3, choices=CondicionComercial,blank=True, null=True)
    forma_entrega =  models.CharField(verbose_name='Forma de entrega',max_length=3, choices=FormaEntrega,blank=True, null=True)
    iva = models.CharField(verbose_name='Condición frente al IVA',max_length=3, choices=IVA,blank=True, null=True)
    tipo_factura = models.CharField(max_length=3, choices=TipoFactura,blank=True, null=True)    
    corredor = models.BooleanField(default=False)
    indirecto = models.BooleanField(default=False)
    agente_perc_iibb = models.BooleanField(verbose_name='Agente percepcion de IIBB',default=False)
    agente_perc_iigg = models.BooleanField(verbose_name='Agente percepcion de IIGG',default=False)
    agente_perc_iva = models.BooleanField(verbose_name='Agente percepcion de IVA',default=False)
    agente_perc_ss = models.BooleanField(verbose_name='Agente percepcion de seguridad social',default=False)
            
    def __str__(self):
        return self.razon_social

    def __unicode__(self):
        return self.razon_social
        
    class Meta:
        ordering = ["razon_social", "nombre_fantasia"]
        verbose_name_plural = " Proveedores"        

class Atributo(models.Model):
    titulo = models.CharField(max_length=50)    
    
    def __str__(self):
        return self.titulo

    def __unicode__(self):
        return self.titulo
        
    class Meta:
        ordering = ("titulo",)
        verbose_name_plural = "Atributos"   
    
class Bien(models.Model): 
    Unidad = [('UN','Unidades'),('KG','Kilogramos'),('MT','Metros'),('LT','Litros')]
          
    codigo = models.CharField(max_length=50)
    denominacion = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=5, choices=Unidad, default='UN')
    clasificador = models.ForeignKey(Clasificador)
    forma_abastecimiento = models.ForeignKey(Abastecimiento)
    importado = models.BooleanField(default=False)
    sin_stock = models.BooleanField(default=False)
    marca = models.ForeignKey(Marca)
    bulto = models.DecimalField (max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=100, blank=True, null=True)
    imagen1 = models.ImageField(verbose_name='Imagen principal', upload_to='Bien/', default='Bien/none.png')    
    imagen2 = models.ImageField(upload_to='Bien/', blank=True)
    imagen3 = models.ImageField(upload_to='Bien/', blank=True)
    imagen4 = models.ImageField(upload_to='Bien/', blank=True)
    imagen5 = models.ImageField(upload_to='Bien/', blank=True)
    proveedor = models.ManyToManyField(Proveedor, through='Compra')
    visible = models.BooleanField(default=True, editable=False)
    atributos = models.ManyToManyField(Atributo, through='BienYAtributo')
    
    def __str__(self):
        return "{0} ({1})".format(self.denominacion, self.codigo)
    
    def costo_base_proveedor(self):
        try: 
            compra = Compra.objects.get(bien=self, base_costeo=True)
            return compra.get_costo_final()
        except MultipleObjectsReturned:
            return 0       
        except ObjectDoesNotExist:
            return 0
            
    def moneda(self):
        try: 
            compra = Compra.objects.get(bien=self, base_costeo=True)
            return compra.moneda
        except MultipleObjectsReturned:
            return None       
        except ObjectDoesNotExist:
            return None
   
    def sign_id(self):
        signer = Signer()
        return signer.sign(self.id)
        
    class Meta:
        ordering = ["codigo", "denominacion"]
        verbose_name_plural = " Bienes"
        permissions = (("action_bien", "Ejecutar acciones"),)

class BienYAtributo(models.Model):
    bien = models.ForeignKey(Bien)
    atributo = models.ForeignKey(Atributo)    
    texto = models.TextField(max_length=9000)
    
    class Meta:             
        unique_together = ('bien', 'atributo') 
    
    def __str__(self):
        return self.bien.denominacion  + "||" + self.atributo.titulo 
        
class Compra(models.Model):
    base_costeo = models.BooleanField()
    proveedor = models.ForeignKey(Proveedor)
    bien = models.ForeignKey(Bien)
    ultima_fecha = models.DateField(auto_now=True)
    bulto = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.SET_NULL, null=True)
    plazo_entrega = models.PositiveSmallIntegerField(blank=True, null=True)
    dto1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dto2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dto3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
      
    def __str__(self):
        return u"%s de: %s" %(self.bien, self.proveedor)
    
    def clean(self):                                      
        if self.base_costeo and self.__class__.objects.filter(Q(base_costeo=True) & Q(bien=self.bien) & ~Q(proveedor=self.proveedor)).exists():# and not self._state:                    
            raise ValidationError("Ya hay un proveedor de base de costeo para este bien.")
        #super(Compra, self).clean(*args, **kwargs)        
        super(Compra, self).clean()

    #def save(self, *args, **kwargs):    
    #    self.full_clean()
    #    return super(Compra, self).save(*args, **kwargs)
    def get_costo_final(self):
        costo = self.costo
        for dto in [self.dto1,self.dto2,self.dto3]:
           if dto:
                costo = costo * (1-dto/100)
        return round(costo,2)
        
        
    class Meta:             
        unique_together = ('proveedor', 'bien')    
        verbose_name = "Costo de proveedor"
        verbose_name_plural = "Costos de proveedores" 
        permissions = (("action_proveedor", "Ejecutar acciones"),)   
                
class Lista(models.Model):
    Tipo = [ ('VTA','Venta'),('VRA', 'Vidriera')]

    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=3, choices=Tipo, default='VTA')
    fecha_vigencia = models.DateField(verbose_name="Fecha de entrada en vigencia")
    moneda = models.ForeignKey(Moneda, on_delete=models.SET_NULL, null=True)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, blank=True, null=True)
    aclaraciones = models.TextField(null=True, blank=True) 
    bienes = models.ManyToManyField(Bien, through='ListaYBien')   
    clasificadores = models.ManyToManyField(Clasificador, through='ListaYClasificador') 
    
    class Meta:
        ordering = ["tipo", "nombre"]
        verbose_name_plural = " Listas"
        permissions = (("action_lista", "Ejecutar acciones"),)

    
    def __str__(self):
        return self.nombre
    
    def get_bienes(self, include_hidden=True, search_bien_id=None, search_string="", clasificador=None, cliente=None):
        if clasificador:
            lista_clasificador = list(self.listayclasificador_set.filter(clasificador=clasificador))
            lista_bien = list(self.listaybien_set.filter(bien__denominacion__icontains=search_string, bien__clasificador = clasificador))        
        else:
            lista_clasificador = list(self.listayclasificador_set.all())
            lista_bien = list(self.listaybien_set.filter(bien__denominacion__icontains=search_string ))
                                                    
        bienes=[]
        
        if cliente:
            if clasificador:
                cliente_clasificador = cliente.clienteyclasificador_set.filter(clasificador=clasificador)
                cliente_bien = cliente.clienteybien_set.filter(bien__denominacion__icontains=search_string, bien__clasificador = clasificador)
            else:
                cliente_clasificador = cliente.clienteyclasificador_set.all()
                cliente_bien = cliente.clienteybien_set.filter(bien__denominacion__icontains=search_string)

            for l in lista_clasificador:
                if not (not include_hidden and not l.visible):
                    for cl in cliente_clasificador:
                        if l.clasificador == cl.clasificador:
                            l.margen = cl.margen
                            cl.margen = -1
                            break

            for cl in cliente_clasificador:
                if cl.margen > 0:
                    new_lista_clasificador = ListaYClasificador(clasificador=cl.clasificador, lista=self, margen=cl.margen, visible=cl.visible)
                    lista_clasificador.append(new_lista_clasificador)
            
            
            for w in lista_bien:
                if not (not include_hidden and not w.visible):
                    if not cliente_clasificador.filter(clasificador=w.bien.clasificador).exists():
                        for bi in cliente_bien:
                            if w.bien == bi.bien:
                                w.margen = bi.margen
                                bi.margen = -1
                                break
                    else:
                        w.margen = -1
                        
            for bi in cliente_bien:
                if bi.margen > 0:
                    new_lista_bien = ListaYBien(bien=bi.bien, lista=self, margen=bi.margen, visible=bi.visible)
                    lista_bien.append(new_lista_bien)      
                    
                                       
        for l in lista_clasificador:
            if not (not include_hidden and not l.visible):
                for b in l.clasificador.bien_set.filter(Q(denominacion__icontains=search_string) | Q(clasificador__denominacion__icontains=search_string)):                      
                    for z in lista_bien:                
                        if z.bien == b and z.margen > 0:                    
                            b.costo = self.calcular_costo(costo=b.costo, margen=z.margen, moneda=z.bien.moneda())                            
                            z.margen = -1
                            break
                    else: #FOR-ELSE, not IF-ELSE!
                        b.costo = self.calcular_costo(costo=b.costo, margen=l.margen, moneda=b.moneda())
                    
                    if b.id == search_bien_id:
                        return b
                    bienes.append(b)
                
        for w in lista_bien:
            if not (not include_hidden and not w.visible):
                if w.margen > 0:
                    w.bien.costo = self.calcular_costo(costo=w.bien.costo, margen=w.margen, moneda=w.bien.moneda())
                    w.bien.visible = w.visible
                
                    if w.bien.id == search_bien_id:
                        return w.bien                    
                    bienes.append(w.bien)    
        
        return sorted(bienes, key=operator.attrgetter('denominacion'))
            
    def calcular_costo(self, costo, margen, moneda):
        try:
            if self.impuesto:
                impuesto = 1+(self.impuesto.valor/100)
            else:
                impuesto = 1
            if moneda.moneda == self.moneda.moneda:
                return round(costo * (1+(margen/100)) * impuesto,2)
            else:    
                return round((costo * (1+(margen/100)) * moneda.cotizacion / self.moneda.cotizacion) * impuesto,2)
        except:
            return 0
            
class ListaYBien(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE )
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE)        
    margen = models.DecimalField(max_digits=10, decimal_places=2)
    visible = models.BooleanField(default = True)

    class Meta:             
        unique_together = ('lista', 'bien') 
    
    def __str__(self):
        return self.lista.nombre + "||" + self.bien.denominacion
    
class ListaYClasificador(models.Model): 
    clasificador = models.ForeignKey(Clasificador, on_delete=models.CASCADE)
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE)        
    #margen = models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(1, message="El descuento tiene que estar entre 0 y 1."),MinValueValidator(0, message="El descuento tiene que estar entre 0 y 1.")])
    margen = models.DecimalField(max_digits=10, decimal_places=2)
    visible = models.BooleanField(default = True)
        
    class Meta:             
        unique_together = ('lista', 'clasificador')

    def __str__(self):
        return self.lista.nombre + "||" + self.clasificador.denominacion

class Expreso(models.Model):
    denominacion = models.CharField(max_length=50 )
    direccion = models.CharField(max_length=100,blank=True, null=True)
    telefono = models.CharField(max_length=50,blank=True, null=True)
    
    def __str__(self):
        return self.denominacion
        
class Cliente(models.Model):    
    #Datos generales
    user = models.OneToOneField(User)
    lista = models.ForeignKey(Lista, on_delete=models.SET_NULL, null=True)
    razon_social = models.CharField(max_length=50)
    nombre_fantasia = models.CharField(max_length=50,blank=True, null=True)
    rubro = models.ForeignKey(Rubro)
    fecha_alta = models.DateField(auto_now_add=True)
    habilitado = models.BooleanField(default=True)
    expreso =  models.ForeignKey(Expreso, on_delete=models.SET_NULL, blank=True, null=True)
    corredor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True)
    telefono = models.CharField(verbose_name="teléfono oficial", max_length=50,blank=True, null=True)
    email = models.EmailField(verbose_name="email oficial", max_length=50,blank=True, null=True)
    website = models.CharField( max_length=100,blank=True, null=True)
    direccion = models.CharField(max_length=100,blank=True, null=True)            
    codigo_postal = models.CharField(max_length=10,blank=True, null=True)
    partido = models.CharField(max_length=50,blank=True, null=True)
    localidad = models.CharField(max_length=50,blank=True, null=True)
    provincia = models.CharField(max_length=50,blank=True, null=True)
    pais = models.CharField(max_length=50,blank=True, null=True)
    contactos = models.ManyToManyField(Contacto,blank=True)        
       
    #Datos comerciales
    cuit = models.CharField(max_length=11, blank=True, null=True, validators=[RegexValidator(r'^\d{1,11}$',message="No cumple con el formato de CUIT/CUIL")])
    comprobante_cuit = models.CharField(max_length=50, blank=True, null=True)    
    condicion_comercial = models.CharField(max_length=3, choices=CondicionComercial,blank=True, null=True)
    informe_economico = models.CharField(max_length=200, blank=True, null=True)
    limite_credito = models.DecimalField(verbose_name="Límite de crédito", max_digits=10, decimal_places=2,blank=True, null=True)
    iva = models.CharField(verbose_name='Condición frente al IVA',max_length=3, choices=IVA,blank=True, null=True)
    forma_entrega =  models.CharField(max_length=3, choices=FormaEntrega,blank=True, null=True)
    alerta = models.TextField(max_length=1000,blank=True, null=True)
    mayorista = models.BooleanField(default=False)
    tipo_factura = models.CharField(max_length=3, choices=TipoFactura,blank=True, null=True)    
    agente_perc_iibb = models.BooleanField(verbose_name='Agente percepcion de IIBB',default=False)
    agente_perc_iigg = models.BooleanField(verbose_name='Agente percepcion de IIGG',default=False)
    agente_perc_iva = models.BooleanField(verbose_name='Agente percepcion de IVA',default=False)
    agente_perc_ss = models.BooleanField(verbose_name='Agente percepcion de seguridad social',default=False)
    jurisdiccion_iibb = models.CharField(max_length=50,blank=True, null=True) 
    
    def __str__(self):
        return self.razon_social

    def __unicode__(self):
        return self.razon_social

    class Meta:
        verbose_name_plural = " Clientes"

class ClienteYClasificador(models.Model):
    clasificador = models.ForeignKey(Clasificador, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)        
    margen = models.DecimalField(max_digits=10, decimal_places=2)
    visible = models.BooleanField(default = True)
        
    class Meta:             
        unique_together = ('cliente', 'clasificador')

    def __str__(self):
        return self.cliente.razon_social + "||" + self.clasificador.denominacion

class ClienteYBien(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)        
    margen = models.DecimalField(max_digits=10, decimal_places=2)
    visible = models.BooleanField(default = True)

    class Meta:             
        unique_together = ('cliente', 'bien') 
    
    def __str__(self):
        return self.cliente.razon_social + "||" + self.bien.denominacion
        
class Pedido(models.Model):
    Status = [ ('ABR','Abierto'),('CHK', 'Confirmado por cliente'),('PRE', 'En preparación'), ('COM', 'Completo'), ('CAN', 'Cancelado')]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_actualizacion = models.DateField(verbose_name='Ult. modificación',auto_now=True)
    fecha_prevista_entrega = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=3, choices=Status, default='ABR')
    bienes = models.ManyToManyField(Bien, through='PedidoYBien')
    vendedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'corredor':True})
    observaciones = models.TextField(null=True, blank=True) 
    
    def get_precio_total(self):   
        total = 0
        for pedidoybien in self.pedidoybien_set.all():
            try:
                costo = self.cliente.lista.get_bienes(search_bien_id=pedidoybien.bien.id, cliente=self.cliente).costo
            except:
                costo = 0
            total += costo * pedidoybien.cantidad
        return total

    def get_cantidad_total(self):
        return self.bienes.all().count()

    def pendientes(self):
        return not self.pedidoybien_set.filter(entregado=False).exists()
    pendientes.boolean = True
    pendientes.short_description = 'Estado pendientes'
    
    def abierto(self):
        return True if self.estado == 'ABR' else False
    
    def cerrado (self):
        return True if self.estado in ('COM','CAN') else False

    def checkout(self):
        self.estado = 'CHK'
            
    def __str__(self):
        return "{0} #{1}".format(str(self.cliente), self.id)

    def __unicode__(self):
        return "{0} #{1}".format(str(self.cliente), self.id)
    
    class Meta:
        verbose_name_plural = " Pedidos"
        permissions = (("action_pedido", "Ejecutar acciones"),)
                
class PedidoYBien(models.Model):
    pedido = models.ForeignKey(Pedido)
    bien = models.ForeignKey(Bien)
    cantidad = models.IntegerField(validators=[MinValueValidator(0, message="Solo cantidades positivas.")])
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    observaciones = models.CharField(max_length=100, null=True, blank=True)
    entregado = models.BooleanField(default=False)
        
    def get_precio(self):
        if self.descuento:
            dto = 1-(self.descuento/100)
        else:
            dto = 1
        try:
            costo = self.pedido.cliente.lista.get_bienes(include_hidden=False, search_bien_id=self.bien.id, cliente=self.pedido.cliente).costo
        except:
            costo = 0
        precio = round(costo * dto,2)
        return precio or 0
        
    def subtotal(self):
        return self.get_precio() * self.cantidad

    def __str__(self):
        return "{0}, bien: {1}, cant: {2}".format(self.pedido, self.bien, self.cantidad)

    def __unicode__(self):
        return "{0}, bien: {1}, cant: {2}".format(self.pedido, self.bien, self.cantidad)