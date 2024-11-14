from django.contrib import admin
from .models import Cliente, Proveedor, Trabajador, Tipo_Usuario, Pais, Estado_Region, Municipio, T_Contribuyente, T_Documento

admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Trabajador)
admin.site.register(Tipo_Usuario)
admin.site.register(Pais)
admin.site.register(Estado_Region)
admin.site.register(Municipio)
admin.site.register(T_Contribuyente)
admin.site.register(T_Documento)
