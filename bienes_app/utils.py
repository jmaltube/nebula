# -*- coding: utf-8 -*-
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import F


#--------------------ADMIN FILTERS--------------------#             

class ItemsPendientesListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Estado pendientes')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'pendientes'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('NO', _('items pendientes')),
            ('YES', _('items entregados')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either 'NO' or 'YES')
        # to decide how to filter the queryset.
        if self.value() == 'NO':
            return queryset.annotate(cantidad=models.Sum('proformaybien__cantidad')).filter(cantidad__lt=F('cantidad_solicitada'))

        if self.value() == 'YES':
            #return queryset.filter(pedidoybien__entregado=False).distinct()
            return queryset.annotate(cantidad=models.Sum('proformaybien__cantidad')).filter(cantidad__gte=F('cantidad_solicitada'))
            

#--------------------MODEL MANAGERS--------------------#             
class PedidoPendientesManager(models.Manager):
    def get_queryset(self):
        return super(PedidoYBienPendienteManager, self).get_queryset().filter(author='Roald Dahl')                                    