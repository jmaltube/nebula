# -*- coding: utf-8 -*-
from django.contrib import admin
from bienes_app.models import (Bien, Proveedor, Compra, Lista, ListaYBien, ListaYClasificador, Clasificador, 
Marca, Abastecimiento, Rubro, Contacto, Cliente, Pedido, PedidoYBien, ClienteYBien, ClienteYClasificador)
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


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ('__all__')
        widgets = {
            'proveedor': autocomplete.ModelSelect2(url='proveedor-autocomplete'),            
      
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


class ClienteYClasificadorInLine(admin.TabularInline):
    model = ClienteYClasificador
    form = ClienteYClasificadorForm
    extra = 1
    verbose_name = "Descuento especial por clasificador"
    verbose_name_plural = "Descuentos especiales por clasificadores"
    #can_delete = False

class PedidoYBienInLine(admin.TabularInline):   
    model = PedidoYBien
    verbose_name_plural = 'Detalle del pedido'
    extra = 1

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
        return HttpResponseRedirect(url+"?ids=%s" % (",".join(selected)))
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
             
#--------------------ADMINS--------------------#             
class ListaAdmin(admin.ModelAdmin):   
    inlines = (ListaYClasificadorInLine,ListaYBienInLine)
    list_display = ('nombre','tipo', 'moneda', 'imprimir')
    list_filter = ['tipo']
    ordering = ['nombre']
    search_fields = ['nombre']    
    actions = [duplicar_lista_action]    
    duplicar_lista_action.short_description = "Duplicar lista(s)"                        
    
    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }

    def imprimir(self, obj):
        url = reverse('imprimir-lista', args=[obj.id])
        return format_html("<a href='"+url+"'>Imprimir</a>")

    imprimir.short_description = 'Impresión'
    imprimir.allow_tags = True
    
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
    
    
    inlines = (CompraInLine,)
    list_display = ('codigo','denominacion','clasificador','marca','costo','moneda',costo_base_proveedor_colored)
    list_filter = ('clasificador', 'proveedor', 'marca')
    list_editable = ['costo']
    ordering = ['clasificador', 'codigo']
    search_fields = ('codigo', 'denominacion')
    actions = [duplicar_bien_action, igualar_costo_bien_action, modificar_costo_bien_action]
    duplicar_bien_action.short_description = "Duplicar bien(es)"
    igualar_costo_bien_action.short_description = "Igualar al costo del proveedor"   
    modificar_costo_bien_action.short_description = "Modificar costo del bien"
    #filter_horizontal = ['bienes']


class ClasificadorAdmin(admin.ModelAdmin):
    readonly_fields = ['get_bienes']
            
    def get_bienes(self, obj):        
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line,) for line in obj.bien_set.all()),
        ) or mark_safe("<span class='errors'>Sin bienes asociados</span>")        
        
    get_bienes.short_description = 'Bienes del clasificador'
    
    
class ProveedorAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos generales',{'fields':('razon_social','nombre_fantasia','telefono','fax','website','email_oficial','tipo','direccion','codigo_postal','partido','localidad','provincia','pais','contactos')}),        
        ('Datos comerciales',{'classes':('collapse',),'fields':('cuit','condicion_comercial','forma_entrega','iva','fecha_incorporacion','tipo_factura','real','indirecto','agente_perc_iibb','agente_perc_iigg','agente_perc_iva','agente_perc_ss')})
    )  
    filter_horizontal = ['contactos']
    
class ClienteAdmin(admin.ModelAdmin):
    inlines = (ClienteYClasificadorInLine, ClienteYBienInLine)    
    filter_horizontal = ['contactos']    
    list_display = ('razon_social', 'nombre_fantasia', 'habilitado')
    list_filter = ['razon_social', 'nombre_fantasia']
    ordering = ['nombre_fantasia']
    search_fields = ['nombre_fantasia']    

    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }
              
class PedidoAdmin(admin.ModelAdmin):   
    inlines = (PedidoYBienInLine,)
    list_display = ('cliente','fecha_actualizacion', 'status', 'checked_out')
    list_filter = ['cliente', 'status']
    ordering = ['cliente', 'fecha_actualizacion']
    search_fields = ['cliente']    
    
    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }

class CompraAdmin(admin.ModelAdmin):
    def get_bien_clasificador(self, obj):
        return obj.bien.clasificador
    get_bien_clasificador.short_description = "clasificador"
        
    list_display = ('proveedor', 'bien', 'get_bien_clasificador', 'costo', 'moneda', 'dto1', 'dto2', 'dto3')
    list_filter = ('proveedor',)
    search_fields = ('bien',)
    ordering = ('proveedor', 'bien')
    list_editable = ('costo',)

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
admin.site.register(Abastecimiento)
admin.site.register(Contacto)
admin.site.register(Pedido, PedidoAdmin)