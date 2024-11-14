from django.contrib import admin
from .models import Cotizacion, Detalles_Cotizacion, Proforma, Detalles_Proforma

admin.site.register(Cotizacion)
admin.site.register(Detalles_Cotizacion)
admin.site.register(Proforma)
admin.site.register(Detalles_Proforma)
