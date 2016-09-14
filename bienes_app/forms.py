# -*- coding: utf-8 -*-
from bienes_app import models
from django.contrib import admin
from django import forms 
from dal import autocomplete
from django.utils.translation import ugettext_lazy, ugettext as _
from django.core.urlresolvers import reverse
from django.utils.html import format_html, format_html_join, mark_safe

#--------------------FORMS--------------------#
class ListaYBienForm(forms.ModelForm):
    class Meta:
        model = models.ListaYBien
        fields = ('__all__')
        widgets = {
            'bien': autocomplete.ModelSelect2(url='bien-autocomplete'),            
      
        }
                
class ListaYClasificadorForm(forms.ModelForm):
    class Meta:
        model = models.ListaYClasificador
        fields = ('__all__')        
        widgets = {
            'clasificador': autocomplete.ModelSelect2(url='clasificador-autocomplete'),                  
        }
        

class ClienteYBienForm(forms.ModelForm):
    class Meta:
        model = models.ClienteYBien
        fields = ('__all__')
        widgets = {
            'bien': autocomplete.ModelSelect2(url='bien-autocomplete'),            
      
        }

class ClienteYClasificadorForm(forms.ModelForm):
    class Meta:
        model = models.ClienteYClasificador
        fields = ('__all__')        
        widgets = {
            'clasificador': autocomplete.ModelSelect2(url='clasificador-autocomplete'),                  
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ('__all__')
        widgets = {
            'corredor': autocomplete.ModelSelect2(url='corredor-autocomplete'),                  
        }

class CompraForm(forms.ModelForm):
    class Meta:
        model = models.Compra
        fields = ('__all__')
        widgets = {
            'proveedor': autocomplete.ModelSelect2(url='proveedor-autocomplete'),            
      
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = models.Pedido
        fields = ('__all__') 
        widgets = {
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete'),
        }

class PedidoYBienForm(forms.ModelForm):
    class Meta:
        model = models.PedidoYBien
        fields = ('__all__')
        widgets = {
            'bien': autocomplete.ModelSelect2(url='bien-autocomplete', forward=['cliente']),
        }

class ProformaForm(forms.ModelForm):
    #autocompletar = forms.BooleanField(required=False)

    class Meta:
        model = models.Proforma
        fields = ('__all__') 
        widgets = {                        
            'pedidos': autocomplete.ModelSelect2Multiple(url='pedido-autocomplete', forward=['cliente']),
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete'),            
        }
    
    def clean_pedidos(self):
        pedidos = self.cleaned_data['pedidos']        
        for pedido in pedidos:
            if not pedido.validado_x_admin:
                raise forms.ValidationError(_("Pedido {0} no está validado por administrador".format(pedido)))
        return pedidos

    def clean_cliente(self):
        cliente = self.cleaned_data['cliente']        
        if not cliente.habilitado:
            raise forms.ValidationError(_("El cliente {0} no está habilitado por administrador".format(cliente)))
        return cliente

 
class ProformaYBienForm(forms.ModelForm):
    class Meta:
        model = models.ProformaYBien
        fields = ('__all__')
        widgets = {                        
            'item': autocomplete.ModelSelect2(url='pedidoybien-autocomplete', forward=['pedidos']),
        }

    def clean_cantidad(self):
        cant = self.cleaned_data['cantidad']
        item = self.cleaned_data['item']
        if cant > item.cantidad_solicitada:
            raise forms.ValidationError(_("La cantidad no puede exceder a la cantidad solicitada"))
        return cant
            

#--------------------INLINES--------------------#         
class ListaYBienInLine(admin.TabularInline):
    model = models.ListaYBien
    form = ListaYBienForm
    extra = 1    
    verbose_name = "Bien"
    verbose_name_plural = "Bienes"                


class ListaYClasificadorInLine(admin.TabularInline):
    model = models.ListaYClasificador
    form = ListaYClasificadorForm
    extra = 1    
    verbose_name = "Clasificador"
    verbose_name_plural = "Clasificadores"                


class CompraInLine(admin.StackedInline):
    model = models.Compra
    form = CompraForm
    extra = 0
    verbose_name = "Opcion de compra"
    verbose_name_plural = "Opciones de compras"

class ClienteYBienInLine(admin.TabularInline):
    model = models.ClienteYBien
    form = ClienteYBienForm
    extra = 1    
    verbose_name = "Descuento especial por bien"
    verbose_name_plural = "Descuentos especiales por bienes"                

class BienYAtributoInLine(admin.TabularInline):
    model = models.BienYAtributo 
    extra = 0    
    verbose_name = "Atributo"
    verbose_name_plural = "Atributos"

class ClienteYClasificadorInLine(admin.TabularInline):
    model = models.ClienteYClasificador
    form = ClienteYClasificadorForm
    extra = 1
    verbose_name = "Descuento especial por clasificador"
    verbose_name_plural = "Descuentos especiales por clasificadores"
    #can_delete = False

class PedidoYBienInLine(admin.TabularInline):   
    model = models.PedidoYBien
    form = PedidoYBienForm
    extra = 1
    verbose_name_plural = _('Detalle del pedido')

    def proformas(self):
        return format_html_join(' ', "<a href='{}'>{}</a>", ((reverse('admin:{}_{}_change'.format(proforma._meta.app_label, proforma._meta.model_name), args=(proforma.pk,)),proforma.pk) for proforma in self.proforma_set.filter(cancelada=False)))
    proformas.short_description = _("Proformas")    

    def cant_pendiente(self):
        #try:
           # cant_pend = self.cantidad_pendiente()
            #if cant_pend > 0:
            #    color = "33CC33"
            #else:
          #  color = "8B0000"
        #except Exception as e:
         #   print(e)
         #   color = "333"
        #return format_html('<span style="color: #{0};">{1}</span>',color,self.cant_pend)
        return self.cantidad_pendiente() or "-"
    cant_pendiente.short_description = _('# PEND.')

    def costo(self):
        return format_html('<span>{}</span> ', self.bien.costo)
    costo.short_description = _("COSTO")

    readonly_fields = (costo, proformas, cant_pendiente, )

    def get_readonly_fields(self, request, obj=None): #OVERRIDE.. DONT RENAME
        if not request.user.is_superuser:
            return self.readonly_fields + ('precio','descuento')
        return self.readonly_fields

class ProformaYBienInLine(admin.TabularInline):
    model = models.ProformaYBien
    form = ProformaYBienForm
    extra = 1
    verbose_name = _("Detalle de la proforma")
    verbose_name_plural = _("Detalle de la proforma")
   

    def precio(self):
        return self.item.precio 
    precio.short_description = _("Precio")
    
    def cantidad_solicitada(self):
        return self.item.cantidad_solicitada
    cantidad_solicitada.short_description = _("# Solic.") 

    def cantidad_pendiente(self):
        return self.item.cantidad_pendiente()
    cantidad_pendiente.short_description = _("# Pend.") 

    readonly_fields = (cantidad_solicitada,cantidad_pendiente,precio,)
    
    #prepopulated_fields = {precio:('bien',)}
