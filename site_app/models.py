# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Moneda(models.Model):
    Moneda = [('ARS','Peso Argentino'),('USD','Dólar'),('EUR','Euro'), ('BRL', 'Real')]
    
    moneda = models.CharField(choices=Moneda, max_length=3, unique=True)
    cotizacion = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return u"%s: %s" %(self.moneda, self.cotizacion)
    
    