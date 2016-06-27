from django.shortcuts import render
from django.template import loader
from django import forms
from bienes_app.models import Lista, Pedido, Bien, PedidoYBien, Clasificador, BienYAtributo
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth import authenticate, login as admin_login, logout as admin_logout
from django.core.signing import Signer
from django.core.mail import mail_admins, send_mail
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy


#////////////////////# PUBLIC #////////////////////# 
def index(request):    
    context = get_base_context(request)
    return render(request, 'index.html',context)
    
def vidriera(request):
    context = get_base_context(request=request) 
    lista = get_lista(request)
    cliente = request.user.cliente if request.user.is_authenticated() else None
    bienes = None

    try:
        search_string = request.session['search_string']                
        clasificador = Clasificador.objects.get(id=request.session['search_clasificador'])
    except:
        clasificador = Clasificador.objects.none()
        search_string = ""
    
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_string = search_form.cleaned_data.get('search_string').strip()
            request.session['search_string'] = search_string
            clasificador = search_form.cleaned_data.get('clasificador')
            request.session['search_clasificador'] = clasificador.id if clasificador else 0
    else:
        search_form = SearchForm({'search_string': search_string, 'clasificador': clasificador})
        search_form.is_valid()
        
    try:
        if lista:
            results = lista.get_bienes(include_hidden=False, search_string=search_string, clasificador=clasificador, cliente=cliente)
            if results:            
                paginator = Paginator(results, 20)
                page = request.GET.get('page') or 1
                bienes = paginator.page(page)
            else:
                search_form.add_error(None, _("No se encontraron resultados"))
                #form.errors['__all__'] = form.error_class(["error msg"])
        else:
            search_form.add_error(None, _("Sin lista de precios asociada"))
    except PageNotAnInteger:
        bienes = paginator.page(1)
    except EmptyPage:
        bienes = paginator.page(paginator.num_pages)

    context['search_form'] = search_form
    context['bienes'] = bienes
    return render(request, 'vidriera.html', context)

def catalogo(request):
    lista = get_lista(request)
    cliente = request.user.cliente if request.user.is_authenticated() else None
    context = get_base_context(request=request)
    signer = Signer()
    signed_id = None
    
    if request.method == 'GET': 
        signed_id = request.GET.get('bien_id',0)        
    else:
        if 'add_to_cart_button' in request.POST:
            signed_id = request.POST.get('bien_id',0)
            add_to_cart(request)

    if signed_id:
        bien_id = int(signer.unsign(signed_id),0)
        if lista and (bien_id > 0):
            bien = lista.get_bienes(include_hidden=False, search_bien_id=bien_id, cliente=cliente)
            context['bien'] = bien
            context['impuesto'] = lista.impuesto
            atributos = BienYAtributo.objects.filter(bien__id=bien.id)
            context['atributos'] = atributos
    return render(request, 'catalogo.html', context)

def pedido(request):
    if request.user.is_authenticated():
        lista = get_lista(request)
        context = get_base_context(request)
        context['carrito'] = get_pedido_detalle(pedido=context['pedido']) 
        context['impuesto'] = lista.impuesto
        return render(request, 'pedido.html',context)
    else:
        return HttpResponseRedirect(reverse('index'))
            
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): 
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                admin_login(request, user)
                return HttpResponseRedirect(reverse('vidriera'))    
            else:                
                login_form.add_error(None, ValidationError(_('Usuario y/o contraseña incorrectos'), code='invalid'))    
    else:
        login_form = LoginForm()
        
    context = get_base_context(request=request)    
    context['login_form'] = login_form
    return render(request, 'login.html',context)
            
def logout(request):
    admin_logout(request)
    return HttpResponseRedirect(reverse('index'))    

    
def add_to_cart(request):
    if request.user.is_authenticated(): 
        signer = Signer()
        cantidad = int(request.POST.get('cantidad'))
        bien_id = int(signer.unsign(request.POST.get('bien_id')),0)
        next_url = request.POST.get('next_url')
        pedido = get_pedido(request)
        try:
            bien = Bien.objects.get(id=bien_id)
            carrito = PedidoYBien.objects.get(pedido=pedido,bien=bien)
            carrito.cantidad = cantidad
        except Bien.DoesNotExist:
            pass    
        except PedidoYBien.DoesNotExist:
            carrito = PedidoYBien(pedido=pedido, bien=bien, cantidad=cantidad)    
        carrito.save()
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseRedirect(reverse('index'))    
        
def remove_from_cart(request):
    if request.user.is_authenticated():
        next_url = request.GET.get('next_url')
        pedido = get_pedido(request)
        signed_id = request.GET.get('bien_id',0)

        if signed_id != 0:
            signer = Signer()
            bien_id = int(signer.unsign(signed_id),0)
            
            try:
                bien = Bien.objects.get(id=bien_id)
                carrito = PedidoYBien.objects.get(pedido=pedido,bien=bien)
                carrito.delete()
            except Bien.DoesNotExist:
                pass    
            except PedidoYBien.DoesNotExist:
                pass
        return HttpResponseRedirect(next_url)    
    else:
        return HttpResponseRedirect(reverse('index'))  

def checkout(request):
    if request.user.is_authenticated():
        try:
            context = get_base_context(request)
            pedido = context['pedido']
            pedido.cerrado = True
            pedido.save()
            subject = _("Nuevo pedido de: ") + str(pedido.cliente)
            
            lista = get_lista(request)
            
            context['carrito'] = get_pedido_detalle(pedido=pedido) 
            context['impuesto'] = lista.impuesto
            
            template = loader.get_template('pedido_email.html')
            
            message = template.render(context)  
            mail_admins(subject=subject , message="yeah",fail_silently=False, connection=None, html_message=message)        
        except Exception as e:
            pass
    
        #print(send_mail(subject="subject", message="message",from_email='juan.altube@nebula.com.ar', recipient_list=('juan.altube@nebula.com.ar',), fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None))
        return HttpResponseRedirect(reverse('pedido'))    
    else:
        return HttpResponseRedirect(reverse('index'))  
        
#////////////////////# PRIVATE #////////////////////#

def get_lista(request):
    try:
        if not request.user.is_authenticated():
            raise ObjectDoesNotExist
        lista = Lista.objects.get(id=request.user.cliente.lista.id)
    except ObjectDoesNotExist:
        lista = Lista.objects.filter(tipo__iexact = 'VRA').last()
    return lista    

def get_pedido(request):
    try:
        pedido = Pedido.objects.filter(cliente=request.user.cliente, entregado=False)[0]       
    except Exception as e:
        pedido = Pedido(cliente=request.user.cliente)
        pedido.save()
    finally:
        return pedido
    

def get_pedido_detalle(pedido):
    pedido_bienes = PedidoYBien.objects.filter(pedido=pedido)
    
    carrito = []
    for item in pedido_bienes:
        precio = item.get_precio()
        bien = {'id': item.bien.sign_id(),
                'denominacion': item.bien.denominacion,
                'codigo': item.bien.codigo,
                'imagen': item.bien.imagen1.url,
                'costo': "{0:.2f}".format(precio),
                'cantidad': item.cantidad,
                'subtotal': "{0:.2f}".format(precio * item.cantidad)
        }
        carrito.append(bien)
    return carrito
    
class LoginForm(forms.Form):
    username = forms.CharField(label=ugettext_lazy("usuario"),max_length=11, required=True)
    password = forms.CharField(label=ugettext_lazy("contraseña"),widget=forms.PasswordInput, required=True) 
    
class SearchForm(forms.Form):

    #categoria_formfield = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset=sitio_categoria.objects.none())
    search_string = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ugettext_lazy('Por nombre o descripción')}), max_length=20, required=False)
    clasificador = forms.ModelChoiceField(empty_label=ugettext_lazy("Clasificadores:"),queryset=Clasificador.objects.all(), required=False)
    
    #def clean(self):
    #    cleaned_data = super(SearchForm, self).clean()
    #    search_string = cleaned_data.get("search_string")
    #    clasificador = cleaned_data.get("clasificador")

    #    if not search_string and not clasificador:
            # Only do something if both fields are valid so far.
    #            raise forms.ValidationError(ugettext_lazy("No se encontraron resultados"))
                
def get_base_context(request):
    pedido = get_pedido(request) if request.user.is_authenticated() else None
    context = {'pedido':pedido,
               'active':resolve(request.path_info).url_name,
               }
    return context
    
def lista_as_json(lista_id):           
    try:
        l = get_lista(request)
        return HttpResponse(serializers.serialize("json", l.get_bienes()))                          
    except MultipleObjectsReturned:
        return        