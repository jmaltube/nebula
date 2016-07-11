#https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class ItemsPendientesListFilter(admin.SimpleListFilter):
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
            ('NO', _('Sin items pendientes')),
            ('YES', _('Con items pendientes')),
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
            return queryset.filter(pedidoybien__entregado=True).distinct()
        if self.value() == 'YES':
            return queryset.filter(pedidoybien__entregado=False).distinct()
                                    