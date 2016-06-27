"""pampero URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
    
Passing named parameters
    url(r'^admin/bienes_app/lista/get-lista/(?P<lista_id>\d+)$',get_lista, name='get-lista'),    
"""
from django.conf.urls import url, include
from django.contrib import admin
from site_app.views import index, vidriera, catalogo, pedido, login, logout, add_to_cart, remove_from_cart, checkout
from bienes_app.views import (BienAutocomplete, ClasificadorAutocomplete, ProveedorAutocomplete,CorredorAutocomplete, duplicar_lista_view, 
                              modificar_costo_view, imprimir_lista)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [    
    url(r'^$', index, name='index'),
    url(r'^vidriera/$', vidriera, name='vidriera'),
    url(r'^catalogo/$', catalogo, name='catalogo'),
    url(r'^pedido/$', pedido, name='pedido'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^add_to_cart/$', add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/$', remove_from_cart, name='remove_from_cart'),
    url(r'^checkout/$', checkout, name='checkout'),    
    url(r'^admin/bienes_app/bien/bien-autocomplete/$',BienAutocomplete.as_view(),name='bien-autocomplete'),
    url(r'^admin/bienes_app/clasificador/clasificador-autocomplete/$',ClasificadorAutocomplete.as_view(),name='clasificador-autocomplete'),    
    url(r'^admin/bienes_app/proveedor/proveedor-autocomplete/$',ProveedorAutocomplete.as_view(),name='proveedor-autocomplete'),    
    url(r'^admin/bienes_app/cliente/corredor-autocomplete/$',CorredorAutocomplete.as_view(),name='corredor-autocomplete'),
    url(r'^admin/bienes_app/duplicar-lista/$',duplicar_lista_view, name='duplicar-lista'),
    url(r'^admin/bienes_app/modificar-costo/$',modificar_costo_view, name='modificar-costo'),
    url(r'^admin/bienes_app/imprimir-lista/(?P<format>\w+)/(?P<lista_id>\d+)/$',imprimir_lista, name='imprimir-lista'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)