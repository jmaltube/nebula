from django.shortcuts import render
from django.template import loader
from django import forms
from bienes_app import models 
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth import authenticate, login as admin_login, logout as admin_logout
from django.core.signing import Signer
from django.core.mail import mail_admins, send_mail
from django.db.models import Q, Count
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.conf import settings
from django.http import HttpResponseServerError


#////////////////////# PUBLIC #////////////////////# 
def index(request):
    context = get_base_context(request)
    lista = get_lista(request)
    try:
        cliente = request.user.cliente if request.user.is_authenticated() else None
        bienes = lista.get_bienes(include_hidden=False, cliente=cliente)
        ids = [bien.id for bien in bienes]  
        top_bienes = models.Bien.objects.filter(pk__in=ids, visible=True).annotate(rank=Count('pedido')).order_by('-rank')[:10]
        context['top_bienes'] = top_bienes 
    except Exception as e:
        pass
    return render(request, 'index.html',context)
    
def vidriera(request):
    context = get_base_context(request=request) 
    lista = get_lista(request)
    try:
        cliente = request.user.cliente if request.user.is_authenticated() else None
    except:
        cliente = None
    bienes = None

    try:
        search_string = request.session['search_string']                
        clasificador = models.Clasificador.objects.get(id=request.session['search_clasificador'])
    except:
        clasificador = models.Clasificador.objects.none()
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
    try:
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
                atributos = models.BienYAtributo.objects.filter(bien__id=bien.id)
                context['atributos'] = atributos
    except AttributeError as e:
        return HttpResponseServerError(e)
    return render(request, 'catalogo.html', context)

def pedido(request):
    try: 
        if request.user.is_authenticated():
            context = get_base_context(request)
            context['pedidos'] = models.Pedido.objects.filter(cliente=request.user.cliente).order_by('id')[:10]
            context['impuesto'] = get_lista(request).impuesto
            return render(request, 'pedido.html',context)
        else:
            return HttpResponseRedirect(reverse('index'))
    except Exception as e:
        print(e)
        return HttpResponseServerError(e)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): 
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                try:
                    if user.cliente.habilitado:
                        admin_login(request, user)
                        return HttpResponseRedirect(reverse('vidriera'))
                except ObjectDoesNotExist as e:
                    login_form.add_error(None, ValidationError(_('No esta asociado a un cliente habilitado'), code='invalid'))
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
            bien = models.Bien.objects.get(id=bien_id)
            carrito = models.PedidoYBien.objects.get(pedido=pedido,bien=bien)
            carrito.cantidad_solicitada = cantidad
        except models.Bien.DoesNotExist:
            pass    
        except models.PedidoYBien.DoesNotExist:
            carrito = models.PedidoYBien(pedido=pedido, bien=bien, cantidad_solicitada=cantidad)    
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
                bien = models.Bien.objects.get(id=bien_id)
                carrito = models.PedidoYBien.objects.get(pedido=pedido,bien=bien)
                carrito.delete()
            except models.Bien.DoesNotExist:
                pass    
            except models.PedidoYBien.DoesNotExist:
                pass
        return HttpResponseRedirect(next_url)    
    else:
        return HttpResponseRedirect(reverse('index'))  

def checkout(request):
    if request.user.is_authenticated():
        try:
            context = get_base_context(request)
            pedido = context['carrito']
            pedido.checkout()
            pedido.save()
            subject = _("Nuevo pedido de: {0} ".format(str(pedido.cliente)))
            lista = get_lista(request)
            context['domain'] = settings.COMPANY_DOMAIN_NAME 
            context['impuesto'] = lista.impuesto
            template = loader.get_template('pedido_email.html')
            message = template.render(context)  
            mail_admins(subject=subject , message="automatic email please do not respond",fail_silently=False, connection=None, html_message=message)        
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
        return models.Lista.objects.get(id=request.user.cliente.lista.id)
    except ObjectDoesNotExist:
        return  models.Lista.objects.filter(tipo__iexact = 'VRA').last()

def get_pedido(request):
    try:
        pedido = models.Pedido.objects.filter(cliente=request.user.cliente, confirmado_x_cliente=False)[0]       
    except:
        try:
            pedido = models.Pedido(cliente=request.user.cliente, confirmado_x_cliente = False, validado_x_admin=True)
            pedido.save()
        except:
            pedido = None
    finally:
        return pedido
        
class LoginForm(forms.Form):
    username = forms.CharField(label=ugettext_lazy("usuario"),max_length=11, required=True)
    password = forms.CharField(label=ugettext_lazy("contraseña"),widget=forms.PasswordInput, required=True) 
    
class SearchForm(forms.Form):

    #categoria_formfield = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset=sitio_categoria.objects.none())
    search_string = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ugettext_lazy('Por nombre o descripción')}), max_length=20, required=False)
    clasificador = forms.ModelChoiceField(empty_label=ugettext_lazy("Clasificadores:"),queryset=models.Clasificador.objects.all(), required=False)
    
    #def clean(self):
    #    cleaned_data = super(SearchForm, self).clean()
    #    search_string = cleaned_data.get("search_string")
    #    clasificador = cleaned_data.get("clasificador")

    #    if not search_string and not clasificador:
            # Only do something if both fields are valid so far.
    #            raise forms.ValidationError(ugettext_lazy("No se encontraron resultados"))
                
def get_base_context(request):
    carrito = get_pedido(request) if request.user.is_authenticated() else None
    context = {'carrito':carrito,
               'empresa': settings.COMPANY_NAME,
               'active':resolve(request.path_info).url_name,
               }
    return context
    
def lista_as_json(lista_id):           
    try:
        l = get_lista(request)
        return HttpResponse(serializers.serialize("json", l.get_bienes()))                          
    except MultipleObjectsReturned:
        return        