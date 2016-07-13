# -*- coding: utf-8 -*-
from django.contrib import admin
from bienes_app.models import (Bien, Proveedor, Compra, Lista, ListaYBien, ListaYClasificador, Clasificador, 
Marca, Abastecimiento, Rubro, Contacto, Cliente, Pedido, PedidoYBien, ClienteYBien, ClienteYClasificador, Expreso, BienYAtributo, Atributo, Impuesto, Moneda)
from dal import autocomplete
from bienes_app.views import duplicar_bien, duplicar_lista, igualar_costo_proveedor
from django.db import transaction
from django import forms 
#from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html, format_html_join, mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from bienes_app.utils import ItemsPendientesListFilter

#--------------------FORMS--------------------#
class ListaYBienForm(forms.ModelForm):
    class Meta:
        model = ListaYBien
        fields = ('__all__')
        widgets = {
            'bien': autocomplete.ModelSelect2(url='bien-autocomplete'),            
      
        }
                
class ListaYClasificadorForm(forms.ModelForm):
    class Meta:
        model = ListaYClasificador
        fields = ('__all__')        
        widgets = {
            'clasificador': autocomplete.ModelSelect2(url='clasificador-autocomplete'),                  
        }
        

class ClienteYBienForm(forms.ModelForm):
    class Meta:
        model = ClienteYBien
        fields = ('__all__')
        widgets = {
            'bien': autocomplete.ModelSelect2(url='bien-autocomplete'),            
      
        }

class ClienteYClasificadorForm(forms.ModelForm):
    class Meta:
        model = ClienteYClasificador
        fields = ('__all__')        
        widgets = {
            'clasificador': autocomplete.ModelSelect2(url='clasificador-autocomplete'),                  
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('__all__')
        widgets = {
            'corredor': autocomplete.ModelSelect2(url='corredor-autocomplete'),                  
        }

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ('__all__')
        widgets = {
            'proveedor': autocomplete.ModelSelect2(url='proveedor-autocomplete'),            
      
        }

class PedidoYBienForm(forms.ModelForm):
    class Meta:
        model = PedidoYBien
        fields = ('__all__')
        widgets = {
            'bien': autocomplete.ModelSelect2(url='bien-autocomplete'),            
      
        }
        
#--------------------INLINES--------------------#         
class ListaYBienInLine(admin.TabularInline):
    model = ListaYBien
    form = ListaYBienForm
    extra = 1    
    verbose_name = "Bien"
    verbose_name_plural = "Bienes"                


class ListaYClasificadorInLine(admin.TabularInline):
    model = ListaYClasificador
    form = ListaYClasificadorForm
    extra = 1    
    verbose_name = "Clasificador"
    verbose_name_plural = "Clasificadores"                


class CompraInLine(admin.StackedInline):
    model = Compra
    form = CompraForm
    extra = 0
    verbose_name = "Opcion de compra"
    verbose_name_plural = "Opciones de compras"

class ClienteYBienInLine(admin.TabularInline):
    model = ClienteYBien
    form = ClienteYBienForm
    extra = 1    
    verbose_name = "Descuento especial por bien"
    verbose_name_plural = "Descuentos especiales por bienes"                

class BienYAtributoInLine(admin.TabularInline):
    model = BienYAtributo 
    extra = 0    
    verbose_name = "Atributo"
    verbose_name_plural = "Atributos"

class ClienteYClasificadorInLine(admin.TabularInline):
    model = ClienteYClasificador
    form = ClienteYClasificadorForm
    extra = 1
    verbose_name = "Descuento especial por clasificador"
    verbose_name_plural = "Descuentos especiales por clasificadores"
    #can_delete = False

class PedidoYBienInLine(admin.TabularInline):   
    model = PedidoYBien
    form = PedidoYBienForm
    extra = 1
    verbose_name_plural = 'Detalle del pedido'

#--------------------ACTIONS--------------------#             
def duplicar_bien_action(modeladmin, request, queryset):
    if request.user.has_perm('bienes_app.action_bien'):    
        for obj in queryset:
            duplicar_bien(model_pk=obj.id)  
    else:
        return HttpResponseRedirect("/admin/bienes_app/bien/")
    
def igualar_costo_bien_action(modeladmin, request, queryset):
    if request.user.has_perm('bienes_app.action_bien'):
        for obj in queryset:
            igualar_costo_proveedor(bien_id=obj.id)        
    else:
        return HttpResponseRedirect("/admin/bienes_app/bien/")
        
def modificar_costo_bien_action(modeladmin, request, queryset): 
    if request.user.has_perm('bienes_app.action_bien'):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        #ct = ContentType.objects.get_for_model(queryset.model)
        url = reverse('modificar-costo')
        return HttpResponseRedirect(url+"?modelo=bien&ids=%s" % (",".join(selected)))
    else:
        return HttpResponseRedirect("/admin/bienes_app/bien/")

def modificar_costo_proveedor_action(modeladmin, request, queryset): 
    if request.user.has_perm('bienes_app.action_proveedor'):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        #ct = ContentType.objects.get_for_model(queryset.model)
        url = reverse('modificar-costo')
        return HttpResponseRedirect(url+"?modelo=proveedor&ids=%s" % (",".join(selected)))
    else:
        return HttpResponseRedirect("/admin/bienes_app/bien/")
        
@transaction.atomic
def duplicar_lista_action(modeladmin, request, queryset): 
    if request.user.has_perm('bienes_app.action_lista'): 
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        url = reverse('duplicar-lista')
        return HttpResponseRedirect(url+"?ids=%s" % (",".join(selected)))
    else:
        return HttpResponseRedirect("/admin/bienes_app/lista/")

def reporte_pedido_pendientes_action(modeladmin, request, queryset): 
    if request.user.has_perm('bienes_app.action_pedido'):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(reverse('reporte-pedido-pendientes', kwargs={'format':'HTML','ids':",".join(selected)}))
    else:
        return HttpResponseRedirect("/admin/bienes_app/pedido/")

#--------------------ADMINS--------------------#             
class ListaAdmin(admin.ModelAdmin):   
    inlines = (ListaYClasificadorInLine,ListaYBienInLine)
    list_display = ('nombre','tipo', 'moneda', 'reporte')
    list_filter = ('tipo',)
    ordering = ('nombre',)
    search_fields = ('nombre',)    
    actions = (duplicar_lista_action,)    
    duplicar_lista_action.short_description = "Duplicar lista(s)"                        
    
    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }

    def reporte(self, obj):
        url_web = reverse('reporte-lista', kwargs={'format':"HTML", 'lista_id':obj.id})
        url_pdf = reverse('reporte-lista', kwargs={'format':"PDF", 'lista_id':obj.id})
        
        return format_html("<a href='{0}'>HTML</a> - <a href='{1}'>PDF</a>".format(url_web, url_pdf))

    reporte.short_description = 'Reporte'
    reporte.allow_tags = True
    
class BienAdmin(admin.ModelAdmin): 
    def costo_base_proveedor_colored(obj):
            if obj.costo_base_proveedor() > obj.costo:
                color = "8B0000"
            else:
                color = "33CC33"
            return format_html('<span style="color: #{0};">{1}</span>',color,obj.costo_base_proveedor())
    costo_base_proveedor_colored.short_description = 'COSTO PROVEEDOR'
    
    fieldsets = ((None, {'fields':('codigo', 'denominacion', 'habilitado', 'costo', 'unidad', 'clasificador', 'forma_abastecimiento', 'importado', 'sin_stock', 'marca', 'bulto')}),
                 ('Imagenes', {'classes':('collapse',), 'fields':('imagen1', 'imagen2','imagen3','imagen4','imagen5')}),    
    )
    
    
    inlines = (BienYAtributoInLine, CompraInLine,)
    list_display = ('codigo','denominacion','clasificador','marca','costo','moneda',costo_base_proveedor_colored)
    list_filter = ('clasificador', 'proveedor', 'marca')
    list_editable = ('costo',)
    ordering = ('clasificador', 'codigo',)
    search_fields = ('codigo', 'denominacion',)
    actions = (duplicar_bien_action, igualar_costo_bien_action, modificar_costo_bien_action,)
    duplicar_bien_action.short_description = "Duplicar bien(es)"
    igualar_costo_bien_action.short_description = "Igualar al costo del proveedor"   
    modificar_costo_bien_action.short_description = "Modificar costo del bien"
    #filter_horizontal = ('bienes')


class ClasificadorAdmin(admin.ModelAdmin):
    readonly_fields = ('get_bienes',)
            
    def get_bienes(self, obj):        
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line,) for line in obj.bien_set.all()),
        ) or mark_safe("<span class='errors'>Sin bienes asociados</span>")        
        
    get_bienes.short_description = 'Bienes del clasificador'
    
    
class ProveedorAdmin(admin.ModelAdmin):
    def get_fecha_alta(self, obj):
        return obj.fecha_alta
    get_fecha_alta.short_description = 'Fecha de alta'
    
    readonly_fields = ('get_fecha_alta',)
    fieldsets = (
        ('Datos generales',{'fields':('razon_social','nombre_fantasia','get_fecha_alta','telefono','fax','website','email','tipo','direccion','codigo_postal','partido','localidad','provincia','pais','contactos')}),        
        ('Datos comerciales',{'classes':('collapse',),'fields':('cuit','condicion_comercial','forma_entrega','iva','tipo_factura','corredor','indirecto','agente_perc_iibb','agente_perc_iigg','agente_perc_iva','agente_perc_ss')})
    )  
    #filter_horizontal = ('contactos')
    
class ClienteAdmin(admin.ModelAdmin):
    def get_fecha_alta(self, obj):
        return obj.fecha_alta
    get_fecha_alta.short_description = 'Fecha de alta'
    
    readonly_fields = ('get_fecha_alta',)
    inlines = (ClienteYClasificadorInLine, ClienteYBienInLine)    
    #filter_horizontal = ('contactos')    
    list_display = ('razon_social', 'nombre_fantasia', 'habilitado')
    list_filter = ('lista',)
    ordering = ('nombre_fantasia',)
    search_fields = ('nombre_fantasia', 'razon_social', 'direccion', 'cuit', 'telefono', 'email', 'localidad', 'provincia' )    
    form = ClienteForm
    fieldsets = (
        ('Datos generales',{'fields':('user','lista','razon_social','nombre_fantasia','rubro','get_fecha_alta','habilitado','expreso','corredor','telefono','email','website','direccion','codigo_postal','partido','localidad','provincia','pais','contactos')}),        
        ('Datos comerciales',{'classes':('collapse',),'fields':('cuit','comprobante_cuit','condicion_comercial','informe_economico','limite_credito','iva','forma_entrega','alerta','mayorista','tipo_factura','agente_perc_iibb','agente_perc_iigg','agente_perc_iva','agente_perc_ss', 'jurisdiccion_iibb')})
    )
    
    
    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }
              
class PedidoAdmin(admin.ModelAdmin):   
    inlines = (PedidoYBienInLine,)
    list_display = ('id','cliente','fecha_actualizacion','fecha_prevista_entrega','estado', 'pendientes')
    list_filter = (ItemsPendientesListFilter, 'estado', 'cliente', 'vendedor', )
    list_editable = ('estado',)
    ordering = ('cliente', 'fecha_actualizacion')
    search_fields = ('cliente', 'vendedor', 'pedido__bien')    
    actions = (reporte_pedido_pendientes_action,)
    reporte_pedido_pendientes_action.short_description = "Reporte de pedidos pendientes"
    
    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }

class CompraAdmin(admin.ModelAdmin):
    def get_bien_clasificador(self, obj):
        return obj.bien.clasificador
    get_bien_clasificador.short_description = "clasificador"
    
    def get_ultima_fecha_modif(self, obj):
        return obj.ultima_fecha
    get_ultima_fecha_modif.short_description = 'Fecha Modif.'
    
    actions = (modificar_costo_proveedor_action,)
    readonly_fields = ('get_ultima_fecha_modif',)
    list_display = ('proveedor', 'bien','get_bien_clasificador', 'get_ultima_fecha_modif', 'base_costeo','costo', 'moneda', 'dto1', 'dto2', 'dto3')
    list_filter = ('proveedor__razon_social','bien__clasificador')
    search_fields = ('proveedor__razon_social','bien__clasificador__denominacion','bien__denominacion','ultima_fecha')
    ordering = ('proveedor', 'bien')
    list_editable = ('costo','dto1', 'dto2', 'dto3')
    modificar_costo_proveedor_action.short_description = "Modificar costo."

class ContactoAdmin(admin.ModelAdmin):
    def clientes(self, obj):
        return ",".join(str(x) for x in obj.cliente_set.all())
    clientes.short_description = 'Clientes'
    
    def proveedores(self, obj):
        return ",".join(str(x) for x in obj.proveedor_set.all())
    proveedores.short_description = 'Proveedores'
    
    list_display = ('nombre_apellido','clientes','proveedores','cargo','telefono','celular','email','horario')
    list_filter = ('cargo',)
    search_fields = ('nombre_apellido','cliente__razon_social','proveedor__razon_social','telefono','celular','email')
    #filter_horizontal = ('bienes')

#--------------------REGISTERS--------------------#
#admin.site.unregister(User)
#admin.site.register(User, UserClienteAdmin)
admin.site.register(Cliente, ClienteAdmin)         
admin.site.register(Bien, BienAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Rubro)
admin.site.register(Compra, CompraAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Clasificador,ClasificadorAdmin)
admin.site.register(Marca)
admin.site.register(Atributo)
admin.site.register(Expreso)
admin.site.register(Abastecimiento)
admin.site.register(Contacto,ContactoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Impuesto)
admin.site.register(Moneda)