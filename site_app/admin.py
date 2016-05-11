from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Permission
from site_app.models import Moneda

#from site_app.models import Cliente

#--------------------INLINES--------------------#             
#class ClienteInLine(admin.StackedInline):   
#    model = Cliente
#    can_delete = False
#    verbose_name_plural = 'Cliente'

#--------------------ADMINS--------------------#             
#class ClienteAdmin(BaseUserAdmin):
#    inlines = (ClienteInLine,)
    
    
#--------------------REGISTERS--------------------#                 
#admin.site.unregister(User)
#admin.site.register(User, ClienteAdmin)
#admin.site.register(Cliente)
admin.site.register(Permission)
admin.site.register(Moneda)