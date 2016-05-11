from django.shortcuts import render
from django import forms
from bienes_app.models import Lista, Pedido, Bien, PedidoYBien, Clasificador
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth import authenticate, login as admin_login, logout as admin_logout
from django.core.signing import Signer


#////////////////////# PUBLIC #////////////////////# 
def index(request):    
    context = get_base_context(request)
    return render(request, 'index.html',context)
    
def vidriera(request):
    lista = get_lista(request)
    cliente = None
    if request.user.is_authenticated():
        cliente = request.user.cliente
    try:
        if lista:
            paginator = Paginator(lista.get_bienes(include_hidden=False, cliente=cliente), 20)
            page = request.GET.get('page')
            if not page:
                page = 1
            bienes = paginator.page(page)
        else:
            bienes = None
    except PageNotAnInteger:
        bienes = paginator.page(1)
    except EmptyPage:
        bienes = paginator.page(paginator.num_pages)
    
    context = get_base_context(request=request)
    context['bienes'] = bienes
    
    return render(request, 'vidriera.html', context)

def catalogo(request):
    lista = get_lista(request)
    cliente = None
    if request.user.is_authenticated():
        cliente = request.user.cliente
    context = get_base_context(request=request)
    signer = Signer()
    signed_id = None
    search_form = SearchForm()
    
    if request.method == 'GET': 
        signed_id = request.GET.get('bien_id',0)        
    else:
        if 'search_button' in request.POST:
            search_form = SearchForm(request.POST)
            
            if search_form.is_valid():
                search_string = search_form.cleaned_data.get('search_string').strip()
                clasificador = search_form.cleaned_data.get('clasificador')
                try:
                    del request.session['results']
                except KeyError:
                    pass       
                         
                bienes = lista.get_bienes(include_hidden=False, search_string=search_string, clasificador=clasificador, cliente=cliente)
                results = [] 
                for bien in bienes:
                    result = {'id': signer.sign(bien.id),
                            'denominacion': bien.denominacion,
                            'imagen': bien.imagen1.url,
                            'costo': "{0:.2f}".format(bien.costo)}
                    results.append(result)           
                
                if results:            
                    request.session['results'] = results
                else:
                    search_form.add_error(None, "No se encontraron resultados")
                context['search_form'] = search_form
        elif 'add_to_cart_button' in request.POST:
            signed_id = request.POST.get('bien_id',0)
            
            add_to_cart(request)

    if signed_id:
        bien_id = int(signer.unsign(signed_id),0)
        if lista and (bien_id > 0):
            bien = lista.get_bienes(include_hidden=False, search_bien_id=bien_id, cliente=cliente)
            context['bien'] = bien
            
    try:
        context['search_form'] = search_form
        context['results'] = request.session['results']
    except KeyError:
        pass
    return render(request, 'catalogo.html', context)


def pedido(request):
    if request.user.is_authenticated():
        lista = get_lista(request)
        context = get_base_context(request)
        pedido_bienes = PedidoYBien.objects.filter(pedido=context['pedido'])
        
        carrito = []
        for item in pedido_bienes:
            precio = item.get_precio()
            bien = {'id': item.bien.sign_id(),
                    'denominacion': item.bien.denominacion,
                    'imagen': item.bien.imagen1.url,
                    'costo': "{0:.2f}".format(precio),
                    'cantidad': item.cantidad,
                    'subtotal': "{0:.2f}".format(precio * item.cantidad)
            }
            carrito.append(bien) 
        context['carrito'] = carrito        
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
                return HttpResponseRedirect(reverse('index'))
            else:                
                login_form.add_error(None, ValidationError('Usuario y/o contraseña incorrectos', code='invalid'))
        context = get_base_context(request, login_form)
        return render(request, 'index.html',context)
        
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
        pedido_id = request.session['pedido']
        pedido = Pedido.objects.get(id=pedido_id)
    except (Pedido.DoesNotExist, KeyError):
        try:
            pedido = Pedido.objects.filter(cliente=request.user.cliente, checked_out=False, completo=False)[0]       
        except: 
            pedido = Pedido(cliente=request.user.cliente)
            pedido.save()
            
    request.session['pedido'] = pedido.id

    return pedido
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=11, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True) 
    
class SearchForm(forms.Form):

    #def __init__(self, *args, **kwargs):
    #    super(SearchForm, self).__init__()
    #    self.lista = kwargs.pop('lista', None)
        #if lista:
        #     self.fields['clasificador'].queryset = lista.clasificadores.all()
    
    #categoria_formfield = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset=sitio_categoria.objects.none())
    search_string = forms.CharField(label='Por nombre o descripción',max_length=20, required=False)
    clasificador = forms.ModelChoiceField(empty_label="Seleccione",queryset=Clasificador.objects.all(), required=False)
    
    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        search_string = cleaned_data.get("search_string")
        clasificador = cleaned_data.get("clasificador")

        if not search_string and not clasificador:
            # Only do something if both fields are valid so far.
                raise forms.ValidationError("No se encontraron resultados")
                
def get_base_context(request, login_form=None):
    if request.user.is_authenticated():
        pedido = get_pedido(request)
    else:
        pedido = None
    if not login_form:
        login_form = LoginForm()
    context = {'pedido':pedido,
               'active':resolve(request.path_info).url_name,
               'login_form':login_form
               }
    return context
    
def lista_as_json(lista_id):           
    try:
        l = get_lista(request)
        return HttpResponse(serializers.serialize("json", l.get_bienes()))                          
    except MultipleObjectsReturned:
        return        