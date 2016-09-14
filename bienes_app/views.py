# -*- coding: utf-8 -*-
from django.shortcuts import render
from dal import autocomplete
from bienes_app import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from copy import deepcopy
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction, IntegrityError
from django import forms
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.conf import settings
#from django.forms.models import model_to_dict
from pdfkit import from_string, configuration
from os import remove 
from django.conf import settings
import datetime
from django.db.models import Q
import json 

#--------------------PRIVATE--------------------#                         

@transaction.atomic
def duplicar_bien(model_pk):
    try:
        #This will raise a DoesNotExist exception if no "id" was found       
        new_bien = deepcopy(models.Bien.objects.get(id=model_pk))    
        new_bien.denominacion = new_bien.denominacion + "--DUPLICADO--"
        new_bien.id = None
        new_bien.save()                
        
        new_proveedores = models.Compra.objects.filter(bien_id=model_pk)
        #with transaction.atomic():
        for proveedor in new_proveedores:
            new_proveedor = deepcopy(proveedor)                                    
            new_proveedor.id = None
            new_proveedor.bien_id = new_bien.id                                                
            new_proveedor.save()                    
                  
    except ObjectDoesNotExist:

        return        
    except IntegrityError:
    
        return

@transaction.atomic
def duplicar_lista(model_pk, margen):    
    try:
        #This will raise a DoesNotExist exception if no "id" was found       
        new_lista = deepcopy(models.Lista.objects.get(id=model_pk))    
        new_lista.nombre = new_lista.nombre + "--DUPLICADO--"
        new_lista.id = None
        new_lista.save()                
        
        new_clasificadores = models.ListaYClasificador.objects.filter(lista_id=model_pk)
        #with transaction.atomic():
        for clasificador in new_clasificadores:
            new_clasificador = deepcopy(clasificador)                                    
            new_clasificador.id = None
            new_clasificador.lista_id = new_lista.id  
            new_clasificador.margen = new_clasificador.margen * (1+(margen/100))
            new_clasificador.save()                    
        
        new_bienes = models.ListaYClasificador.objects.filter(lista_id=model_pk)
        for bien in new_bienes:
            new_bien = deepcopy(bien)                                    
            new_bien.id = None
            new_bien.lista_id = new_lista.id                                    
            new_bien.margen = new_bien.margen * (1+(margen/100))            
            new_bien.save()                    
                
    except ObjectDoesNotExist:        
        return        
    except IntegrityError:
    
        return

    
def igualar_costo_proveedor(bien_id):
    try:
        bien = models.Bien.objects.get(id=bien_id)
        bien.costo = bien.costo_base_proveedor()
        bien.save()
    except MultipleObjectsReturned:
        return
        
                
def modificar_costo_bien(bien_id, tipo, valor):
    try:
        bien = models.Bien.objects.get(id=bien_id)
        if tipo == 'POR':
            bien.costo = bien.costo * (1+(valor/100))
        elif tipo == 'VAL':
            bien.costo = bien.costo + valor
        
        bien.save()
    except MultipleObjectsReturned:
        return

def modificar_costo_proveedor(id, tipo, valor):
    try:
        opcion_proveedor = models.Compra.objects.get(id=id)
        if tipo == 'POR':
            opcion_proveedor.costo = opcion_proveedor.costo * (1+(valor/100))
        elif tipo == 'VAL':
            opcion_proveedor.costo = opcion_proveedor.costo + valor
        
        opcion_proveedor.save()
    except MultipleObjectsReturned:
        return      
        
def generate_pdf(request, template_path, context, file_name):
    html_template = get_template(template_path)
    rendered_html = html_template.render(request=request, context=context)#.encode(encoding="UTF-8")
    options = {
        'page-size': 'Letter',
        'margin-top': '0.25in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
    } #'no-outline': None
    css = '{0}/css/base.css'.format(settings.STATICFILES_DIRS[0])
    pdf_name = "{0}/pdf/{1}.pdf".format(settings.STATICFILES_DIRS[0], file_name)
    config = configuration(wkhtmltopdf=bytes(settings.PATH_TO_WKHTMLTOPDF, 'utf-8'))
    from_string(rendered_html, pdf_name, options=options, css=css, configuration=config)
    pdf = open(pdf_name,mode='rb')#,encoding = "ISO-8859-1")
    response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
    response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(file_name)
    pdf.close()
    remove(pdf_name)  # remove the locally created pdf file.
    return response              

#--------------------FORMS--------------------#

class DuplicarListaForm(forms.Form):
    margen = forms.DecimalField(label="Modificar margen (%)",max_digits=10, decimal_places=2,required=True, initial=0)
    ids = forms.CharField(widget = forms.HiddenInput())#, required = False)
    margen.help_text = "Deje el margen igual a cero para mantener el margen de la lista."


class ModificarCostoForm(forms.Form):
    Tipo = [('POR','Porcentaje'), ('VAL','Valor fijo')]
    tipo = forms.ChoiceField(label="Modificar por",choices=Tipo, required=True)   
    valor = forms.DecimalField(label="valor",help_text="0-100 para (%) <br> 0-99999999.99 para valores fijos",max_digits=10, decimal_places=2,required=True, initial=10)
    ids = forms.CharField(widget = forms.HiddenInput())#, required = False)
    modelo = forms.CharField(widget = forms.HiddenInput())


#--------------------PUBLIC AUTOCOMPLETES--------------------#

class BienAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Bien.objects.none()

        cliente_fwd = self.forwarded.get('cliente', None)
        
        if cliente_fwd:
            try:    
                cliente = models.Cliente.objects.get(id=int(cliente_fwd))
                qs = cliente.lista.get_bienes(include_hidden=False, search_string=self.q, cliente=cliente)
            except Exception as e:
                print("exception in autocomplete bienes: {0}".format(e))
                return models.Bien.objects.none()
        else:
            qs = models.Bien.objects.filter(habilitado=True)
        
            if self.q:
                qs = qs.filter(Q(denominacion__icontains=self.q) | Q(codigo__icontains=self.q))
                
        return qs
        
class ClasificadorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Clasificador.objects.none()
            
        qs = models.Clasificador.objects.all()
        
        if self.q:
            qs = qs.filter(denominacion__icontains=self.q)
            
        return qs        


class ProveedorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Proveedor.objects.none()
            
        qs = models.Proveedor.objects.filter(habilitado=True)
        
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
            
        return qs

class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Cliente.objects.none()
            
        try:
            vendedor = models.Proveedor.objects.get(user=self.request.user) 
            qs = models.Cliente.objects.filter(habilitado=True,corredor=vendedor)
        except:
            qs = models.Cliente.objects.filter(habilitado=True)
            
        if self.q:
            qs = qs.filter(Q(razon_social__icontains=self.q) | Q(nombre_fantasia__icontains=self.q))
            
        return qs

class CorredorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Proveedor.objects.none()
            
        qs = models.Proveedor.objects.filter(habilitado=True, corredor=True)
        
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
            
        return qs


class PedidoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.Pedido.objects.none()

        cliente_fwd = self.forwarded.get('cliente', None)
        
        if cliente_fwd:
            try:    
                cliente = models.Cliente.objects.get(id=int(cliente_fwd))
                qs = models.Pedido.objects.filter(cliente=cliente,confirmado_x_cliente=True, presupuesto=False)
            except Exception as e:
                print("exception in autocomplete pedidos: {0}".format(e))
                return models.Pedido.objects.none()
        else:    
            qs = models.Pedido.objects.filter(confirmado_x_cliente=True)
        
        if self.q:
            qs = qs.filter(cliente__razon_social=self.q)
            
        return qs        

class PedidoYBienAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return models.PedidoYBien.objects.none()

        pedidos_fwd = self.forwarded.get('pedidos', None)
        if pedidos_fwd:
            try:    
                ids = [int(pedido) for pedido in pedidos_fwd]
                qs = models.PedidoYBien.objects.filter(pedido_id__in=ids)
                #qs = [pb.bien for pb in pedidoybienes]
            except Exception as e:
                print("exception in autocomplete pedidoybienes: {0}".format(e))
                return models.PedidoYBien.objects.none()
        else:
            qs = models.PedidoYBien.objects.all()

        if self.q:
            qs = qs.filter(bien__denominacion__icontains=self.q)
            
        return qs        

#--------------------REPORTS--------------------#

@login_required(login_url='/admin/login/')
def reporte_lista(request, lista_id=None, format='HTML'):
    try:
        l = models.Lista.objects.get(id=int(lista_id))
        lista = l.get_bienes()
        context = {'title':l.nombre,'lista':lista, 'opts':models.Lista._meta}
        if format == "HTML":
            return render(request, 'reports/lista.html',context=context)
        elif format == "PDF":
            file_name = "Lista_{0}_{1}".format(l.nombre, str(datetime.date.today()))            
            return generate_pdf(request,'reports/lista.html',context, file_name )
    except Exception as e:
        return HttpResponseServerError(e)
        
@login_required(login_url='/admin/login/')
def reporte_pedido_pendientes(request, ids=None, format='HTML'):
    try:
        pedidos = models.Pedido.objects.filter(id__in=ids.split(',')).exclude(estado__in=['CAN', 'COM']).filter( pedidoybien__entregado=False).distinct()
        context = {'title':'Lista de pedidos con pendientes','pedidos':pedidos,'opts':models.Pedido._meta}

        if format == "HTML":
            pdf_url = reverse('reporte-pedido-pendientes', kwargs={'format':'PDF','ids':ids})
            context['pdf_url'] = pdf_url
            return render(request, 'reports/pedido_pendientes.html',context=context)
        elif format == "PDF":            
            file_name = "Pedido_pendientes_{0}".format(str(datetime.date.today()))
            return generate_pdf(request,'reports/pedido_pendientes.html',context, file_name )
    except Exception as e:
        return HttpResponseRedirect('/admin/bienes_app/pedido/')

@login_required(login_url='/admin/login/')
def popup_pedidos_pendientes(request, pedido_id):
    try:
        if request.is_ajax():
            id = int(pedido_id,0)
            pedido = models.Pedido.objects.get(id=id)
            context = {'pedido':pedido} 
            return render(request, 'reports/pedido_pendientes_popup.html', context=context)
        else:
            raise Exception("not an ajax request.")
    except Exception as e:
        return HttpResponseServerError(e)

#--------------------AJAX--------------------#

@login_required(login_url='/admin/login/')
def proformaybien_inline_autocomplete(request):
    try:
        if request.is_ajax():
            id = int(request.GET.get('item'),0)
            item = models.PedidoYBien.objects.get(id=id)
            data = {'cant_solic': item.cantidad_solicitada,
                    'cant_pend':item.cantidad_pendiente(),                    
                    'precio':str(item.precio),                    
                    }
            json_response = json.dumps(data)
            return HttpResponse(json_response, content_type='application/json')
        else:
            raise Exception("not an ajax request.")
    except Exception as e:
        return HttpResponseServerError(e)


@login_required(login_url='/admin/login/')
def proforma_autocomplete(request):
    try:
        #if request.is_ajax():
            pedidos = [item for item in request.GET.get('pedidos').split(',')]
            pedido_y_bien = models.PedidoYBien.objects.filter(pedido__in=pedidos)
            items = {str(item.pk):{
                    'value':item.pk,
                    'text':str(item),
                    'cant_solic': item.cantidad_solicitada,
                    'cant_pend':item.cantidad_pendiente(),                    
                    'precio':str(item.precio)
                    } for item in pedido_y_bien }
            data = {'items': items}
            json_response = json.dumps(data)
            return HttpResponse(json_response, content_type='application/json')
        #else:
        #    raise Exception("not an ajax request.")
    except Exception as e:
        return HttpResponseServerError(e)


@login_required(login_url='/admin/login/')
def pedidoybien_inline_autocomplete(request):
    try:
        if request.is_ajax():
            bien_id = int(request.GET.get('bien'),0)
            cliente_id = int(request.GET.get('cliente'),0)
            if bien_id and cliente_id:
                bien = models.Bien.objects.get(id=bien_id)
                cliente = models.Cliente.objects.get(id=cliente_id)
                precio = cliente.lista.get_bienes(include_hidden=False, search_bien_id=bien.id, cliente=cliente).costo
                costo = bien.costo
                data = {'precio':str(precio),
                        'costo':str(costo),
                        }
                json_response = json.dumps(data)
                return HttpResponse(json_response, content_type='application/json')
            else:
                raise Exception("Error con ajax data")
        else:
            raise Exception("not an ajax request.")
    except Exception as e:
        return HttpResponseServerError(e)     

#--------------------ACTIONS--------------------#
@login_required(login_url='/admin/login/')
def duplicar_lista_view(request):
    if request.method == 'POST':
        form = DuplicarListaForm(request.POST)
        if form.is_valid():
            new_margen = form.cleaned_data['margen']
            ids = form.cleaned_data['ids'].split(",")
            
            for id in ids:                
                duplicar_lista(model_pk=id, margen=new_margen)
            
            return HttpResponseRedirect('/admin/bienes_app/lista/')
    else:        
        form = DuplicarListaForm()        
        form.fields['ids'].initial = request.GET.get('ids')              
    return render(request, 'forms/duplicar_lista.html', {'title':'Duplicar lista','form':form, 'opts':models.Lista._meta})        
    
@login_required(login_url='/admin/login/')
def modificar_costo_view(request):
    if request.method == 'POST':
        form = ModificarCostoForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            valor = form.cleaned_data['valor']
            ids = form.cleaned_data['ids'].split(",")
            modelo = form.cleaned_data['modelo']
            
            if modelo == 'bien': 
                for id in ids:                
                    modificar_costo_bien(bien_id=id, tipo=tipo, valor=valor)
                return HttpResponseRedirect('/admin/bienes_app/bien/')
            elif modelo == 'proveedor':
                for id in ids:                
                    modificar_costo_proveedor(id=id, tipo=tipo, valor=valor)
                return HttpResponseRedirect('/admin/bienes_app/compra/')
    else:        
        form = ModificarCostoForm()        
        form.fields['ids'].initial = request.GET.get('ids')
        form.fields['modelo'].initial = request.GET.get('modelo')
        
    return render(request, 'forms/modificar_costo.html', {'title':'Modificar costo','form':form,'opts':models.Bien._meta})    

@login_required(login_url='/admin/login/')
@transaction.atomic
def generar_proforma_view(request, pedido_ids):
    if request.method == 'GET':
        ids = pedido_ids.split(",")
        for i,id in enumerate(ids):
            pedido = models.Pedido.objects.get(id=id)
            if not i:
                proforma = models.Proforma(cliente=pedido.cliente)
                proforma.save()
            proforma.pedidos.add(pedido)
            for item in pedido.pedidoybien_set.all():
                proforma_y_bien = models.ProformaYBien(proforma=proforma, item=item, cantidad=item.cantidad_pendiente())                
                proforma_y_bien.save()
        return HttpResponseRedirect(reverse("admin:{0}_{1}_change".format(models.Proforma._meta.app_label, models.Proforma._meta.model_name),args=(proforma.pk,)))