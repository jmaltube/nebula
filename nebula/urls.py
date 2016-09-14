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
from site_app import views as site_views
from bienes_app import views as bienes_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [    
    url(r'^$', site_views.index, name='index'),
    url(r'^vidriera/$', site_views.vidriera, name='vidriera'),
    url(r'^catalogo/$', site_views.catalogo, name='catalogo'),
    url(r'^pedido/$', site_views.pedido, name='pedido'),
    url(r'^login/$', site_views.login, name='login'),
    url(r'^logout/$', site_views.logout, name='logout'),
    url(r'^add_to_cart/$', site_views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/$', site_views.remove_from_cart, name='remove_from_cart'),
    url(r'^checkout/$', site_views.checkout, name='checkout'),    
    url(r'^admin/bienes_app/forms/bien/bien-autocomplete/$',bienes_views.BienAutocomplete.as_view(),name='bien-autocomplete'),
    url(r'^admin/bienes_app/forms/clasificador/clasificador-autocomplete/$',bienes_views.ClasificadorAutocomplete.as_view(),name='clasificador-autocomplete'),    
    url(r'^admin/bienes_app/forms/proveedor/proveedor-autocomplete/$',bienes_views.ProveedorAutocomplete.as_view(),name='proveedor-autocomplete'),    
    url(r'^admin/bienes_app/forms/cliente/corredor-autocomplete/$',bienes_views.CorredorAutocomplete.as_view(),name='corredor-autocomplete'),
    url(r'^admin/bienes_app/forms/cliente/cliente-autocomplete/$',bienes_views.ClienteAutocomplete.as_view(),name='cliente-autocomplete'),
    url(r'^admin/bienes_app/forms/pedido/pedido-autocomplete/$',bienes_views.PedidoAutocomplete.as_view(),name='pedido-autocomplete'),
    url(r'^admin/bienes_app/forms/pedido/pedidoybien-autocomplete/$',bienes_views.PedidoYBienAutocomplete.as_view(),name='pedidoybien-autocomplete'),
    url(r'^admin/bienes_app/forms/pedido/pedidoybien-inline-autocomplete/$',bienes_views.pedidoybien_inline_autocomplete,name='pedidoybien-inline-autocomplete'),    
    url(r'^admin/bienes_app/forms/proforma/proformaybien-inline-autocomplete/$',bienes_views.proformaybien_inline_autocomplete,name='proformaybien-inline-autocomplete'),    
    url(r'^admin/bienes_app/forms/proforma/proforma-autocomplete/$',bienes_views.proforma_autocomplete,name='proforma-autocomplete'),    
    url(r'^admin/bienes_app/actions/duplicar-lista/$',bienes_views.duplicar_lista_view, name='duplicar-lista'),
    url(r'^admin/bienes_app/actions/modificar-costo/$',bienes_views.modificar_costo_view, name='modificar-costo'),
    url(r'^admin/bienes_app/actions/generar-proforma/(?P<pedido_ids>\d+(,\d+)*)/$',bienes_views.generar_proforma_view, name='generar-proforma'),
    url(r'^admin/bienes_app/reports/reporte-lista/(?P<format>\w+)/(?P<lista_id>\d+)/$',bienes_views.reporte_lista, name='reporte-lista'),
    url(r'^admin/bienes_app/reports/reporte-pedido-pendientes/(?P<format>\w+)/(?P<ids>\d+(,\d+)*)/$',bienes_views.reporte_pedido_pendientes, name='reporte-pedido-pendientes'),
    url(r'^admin/bienes_app/reports/popup-pedidos-pendientes/(?P<pedido_id>\d+)/$',bienes_views.popup_pedidos_pendientes, name='popup-pedidos-pendientes'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
] 

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)