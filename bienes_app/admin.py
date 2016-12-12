# -*- coding: utf-8 -*-
from django.contrib import admin
from bienes_app import models
from bienes_app.views import duplicar_bien, duplicar_lista, igualar_costo_proveedor
from django.db import transaction
#from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html, format_html_join, mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from bienes_app.utils import ItemsPendientesListFilter
from bienes_app import forms as admin_forms
from django.conf import settings
from django.utils.translation import ugettext_lazy, ugettext as _
from django.db.models import F
from django.db import models as db_models
from django.db.models.functions import Coalesce

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

def generar_proforma_action(modeladmin, request, queryset):
    if request.user.has_perm('bienes_app.action_pedido'):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(reverse('generar-proforma', kwargs={'pedido_ids':",".join(selected)}))
    else:
        return HttpResponseRedirect("/admin/bienes_app/pedido/")

def enviar_pedido_valorizado_action(modeladmin, request, queryset):
    if request.user.has_perm('bienes_app.action_pedido'):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(reverse('enviar-pedido-valorizado', kwargs={'pedido_ids':",".join(selected)}))
    else:
        return HttpResponseRedirect("/admin/bienes_app/pedido/")

#--------------------ADMINS--------------------#
class ListaAdmin(admin.ModelAdmin):
    inlines = (admin_forms.ListaYClasificadorInLine,admin_forms.ListaYBienInLine)
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

    fieldsets = ((None, {'fields':('codigo', 'denominacion', 'habilitado', 'costo', 'unidad', 'clasificador', 'forma_abastecimiento', 'importado', 'sin_stock','marca', 'bulto')}),
                 ('Imagenes', {'classes':('collapse',), 'fields':('imagen1', 'imagen2','imagen3','imagen4','imagen5')}),
    )


    inlines = (admin_forms.BienYAtributoInLine, admin_forms.CompraInLine,)
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
        ('Datos generales',{'fields':('user','razon_social','nombre_fantasia','get_fecha_alta','telefono','fax','website','email','tipo','direccion','codigo_postal','pais','provincia','localidad','contactos','r','e','primeros_4_digitos')}),
        ('Datos comerciales',{'classes':('collapse',),'fields':('cuit','condicion_comercial','forma_entrega','iva','tipo_factura','corredor','indirecto','agente_perc_iibb','agente_perc_iigg','agente_perc_iva','agente_perc_ss')})
    )
    #filter_horizontal = ('contactos')

class ClienteAdmin(admin.ModelAdmin):
    def get_fecha_alta(self, obj):
        return obj.fecha_alta
    get_fecha_alta.short_description = 'Fecha de alta'

    readonly_fields = ('get_fecha_alta',)
    inlines = (admin_forms.ClienteYClasificadorInLine, admin_forms.ClienteYBienInLine)
    #filter_horizontal = ('contactos')
    list_display = ('razon_social', 'nombre_fantasia', 'habilitado')
    list_filter = ('lista',)
    ordering = ('nombre_fantasia',)
    search_fields = ('nombre_fantasia', 'razon_social', 'direccion', 'cuit', 'telefono', 'email', 'localidad', 'provincia' )
    form = admin_forms.ClienteForm
    fieldsets = (
        ('Datos generales',{'fields':('user','lista','razon_social','nombre_fantasia','rubro','get_fecha_alta','habilitado','expreso','corredor','telefono','email','website','direccion','codigo_postal','pais','provincia','localidad','contactos')}),
        ('Datos comerciales',{'classes':('collapse',),'fields':('cuit','comprobante_cuit','condicion_comercial','informe_economico','limite_credito','iva','forma_entrega','alerta','mayorista','tipo_factura','agente_perc_iibb','agente_perc_iigg','agente_perc_iva','agente_perc_ss', 'jurisdiccion_iibb')})
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('habilitado',)
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs): #Para que el pedido esté habilitado x defecto si el user es un admin
        form = super(ClienteAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            form.base_fields['habilitado'].initial = True
        return form

    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }

class PedidoAdmin(admin.ModelAdmin):

    def pendientes_popup(self):
        if self.pendientes():
            return format_html('''
            <div id="popup{0}" class="popup">
                <span class="button b-close"><span>x</span></span>
                <div class="content{0}" style="height: auto; width: auto;"></div>
            </div>
            <img id="popimg{0}" src="{2}admin/img/icon-no.svg" alt="XXX" title="Click para mas info"  data-id={0} data-url={1} />
            '''
            ,self.pk,reverse('popup-pedidos-pendientes', kwargs={'pedido_id':self.pk}),settings.STATIC_URL)
        else:
            return format_html('<img src="{}admin/img/icon-yes.svg" alt="OK" />',settings.STATIC_URL)

    inlines = (admin_forms.PedidoYBienInLine,)
    list_display = ('id','cliente','fecha_creacion','fecha_actualizacion','fecha_prevista_entrega','presupuesto',pendientes_popup )#'estado', 'pendientes')
    list_filter = (  'cliente', 'vendedor', ) #'estado',ItemsPendientesListFilter
    exclude = ('confirmado_x_cliente',)
    ordering = ('-fecha_creacion','cliente', 'fecha_actualizacion')
    search_fields = ('cliente', 'vendedor', 'pedido__bien')
    actions = (reporte_pedido_pendientes_action, enviar_pedido_valorizado_action, generar_proforma_action,)
    reporte_pedido_pendientes_action.short_description = "Reporte de pedidos pendientes"
    form = admin_forms.PedidoForm
    readonly_fields = ('fecha_creacion','estado_pendientes','precio_total', 'costo_total', 'utilidad')
    generar_proforma_action.short_description = _("Generar proforma")

    fieldsets = (
        (_('DATOS ENCABEZADO'),{'fields':('cliente', 'estado_pendientes', 'precio_total', 'costo_total', 'utilidad')}),
        (_('Mas opciones'),{'classes':('collapse',),'fields':('fecha_creacion','fecha_prevista_entrega', 'presupuesto', 'validado_x_admin', 'vendedor', 'observaciones')})
    )

    def estado_pendientes(self, obj):
        boolean = "no" if obj.pendientes() else "yes"
        return format_html('<img src="{}admin/img/icon-{}.svg" alt="False" />',settings.STATIC_URL, boolean)
    estado_pendientes.short_description = 'Estado pendientes'

    def precio_total(self, obj):
        return obj.get_precio_total()

    def costo_total(self, obj):
        return obj.get_costo_total()

    def utilidad(self, obj):
        return "%"

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('validado_x_admin',)
        return self.readonly_fields

    def get_queryset(self, request): #Para filtrar el query del admin
        qs = super(PedidoAdmin, self).get_queryset(request).filter(confirmado_x_cliente=True)
        if request.user.is_superuser:
            return qs
        else:
            try:
                return qs.filter(cliente__corredor__user=request.user)
            except Exception as e:
                print(e)
                return qs.none()

    def get_form(self, request, obj=None, **kwargs): #Para que el pedido esté validado x defecto si el user es un admin
        form = super(PedidoAdmin, self).get_form(request, obj, **kwargs)
        try:
            if request.user.is_superuser:
                form.base_fields['validado_x_admin'].initial = True
            vendedor = models.Proveedor.objects.get(user=request.user)
            form.base_fields['vendedor'].initial = vendedor
        except:
            pass
        return form

    def has_delete_permission(self, request, obj=None):
        perm = super(PedidoAdmin, self).has_delete_permission(request, obj)
        if obj and obj.proforma_set.filter(cancelada=False):
            return False
        return perm


    def get_actions(self, request): #Disable delete
        actions = super(PedidoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    class Media:
        css = { "all" : ("css/hide_admin_original.css", 'css/bpopup.style.min.css')}
        js = ('js/jquery.bpopup.min.js','js/ajax_pedido.js')

class PedidoItemsAdmin(admin.ModelAdmin):
    def cant_pendiente(obj):
        return obj.cantidad_pendiente()

    def precio_total(obj):
        return obj.subtotal_pendiente()

    def fecha_prevista_entrega(obj):
        return obj.pedido.fecha_prevista_entrega

    readonly_fields = (cant_pendiente, precio_total, fecha_prevista_entrega)
    list_display = ('pedido', 'bien', cant_pendiente,precio_total,'observaciones', fecha_prevista_entrega)
    list_filter = ('bien__clasificador', 'bien__clasificador__rubro__denominacion')#ItemsPendientesListFilter,)
    search_fields = ('pedido__cliente__razon_social','bien__clasificador__denominacion','bien__denominacion', 'bien__codigo')
    #ordering = (fecha_prevista_entrega)
    #list_editable = ('costo','dto1', 'dto2', 'dto3')
    #modificar_costo_proveedor_action.short_description = "Modificar costo."

    def get_queryset(self, request): #Para filtrar el query del admin
        try:
            qs = super(PedidoItemsAdmin, self).get_queryset(request)
            if request.user.is_superuser:
                return qs.annotate(cantidad=Coalesce(db_models.Sum('proformaybien__cantidad'),0)).filter(cantidad__lt=F('cantidad_solicitada'),pedido__confirmado_x_cliente=True, pedido__presupuesto=False )
            else:
                raise Exception
        except Exception as e:
            print(e)
            return qs.none()

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


class ProformaAdmin(admin.ModelAdmin):
    def get_self(self):
        return self
    get_self.short_description = _("Proforma")

    def proforma_cancelada(self):
        if self.cancelada:
            return format_html('''
            <img src="{0}admin/img/icon-no.svg" alt="XXX" title="Proforma CANCELADA" "/>
            '''
            ,settings.STATIC_URL)
        else:
            return ""
    proforma_cancelada.short_description = ""

    list_display = (get_self,'cliente', 'fecha_creacion', 'factura', 'observaciones',proforma_cancelada)
    list_filter = ('cliente',)
    search_fields = ('cliente__razon_social', 'factura')
    inlines = (admin_forms.ProformaYBienInLine,)
    readonly_fields = ('autocompletar',)
    form = admin_forms.ProformaForm

    fieldsets = (
        (_('DATOS ENCABEZADO'),{'fields':('cliente', 'pedidos', 'autocompletar')}),
        (_('Mas opciones'),{'classes':('collapse',),'fields':('factura', 'observaciones', 'cancelada')})
    )

    #def render_change_form(self, request, context, *args, **kwargs): #Esto es para filtrar el query de un m2m field al iniciar el formulario.
    #     context['adminform'].form.fields['pedidos'].queryset = models.Pedido.objects.filter(id=39)

    #     return super(ProformaAdmin, self).render_change_form(request, context, *args, **kwargs)

    def autocompletar(self, obj):
        return format_html('<a id="Autocompletar" class="button">Autocompletar</a>')
    autocompletar.short_description = ' '

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('validado_x_admin',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        perm = super(ProformaAdmin, self).has_delete_permission(request, obj)
        return False

    def get_actions(self, request): #Disable delete
        actions = super(ProformaAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    #def save_model(self, request, obj, form, change):

    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }
        js = ('js/ajax_proforma.js',)

#--------------------REGISTERS--------------------#
#admin.site.unregister(User)
#admin.site.register(User, UserClienteAdmin)
admin.site.register(models.Cliente, ClienteAdmin)
admin.site.register(models.Bien, BienAdmin)
admin.site.register(models.Proveedor, ProveedorAdmin)
admin.site.register(models.Rubro)
admin.site.register(models.Pais)
admin.site.register(models.Provincia)
admin.site.register(models.Localidad)
admin.site.register(models.Comprobantes)
admin.site.register(models.Compra, CompraAdmin)
admin.site.register(models.Lista, ListaAdmin)
admin.site.register(models.Clasificador,ClasificadorAdmin)
admin.site.register(models.Marca)
admin.site.register(models.Atributo)
admin.site.register(models.Expreso)
admin.site.register(models.Abastecimiento)
admin.site.register(models.Contacto,ContactoAdmin)
admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.PedidoYBien, PedidoItemsAdmin)
admin.site.register(models.Impuesto)
admin.site.register(models.Moneda)
admin.site.register(models.Proforma, ProformaAdmin)