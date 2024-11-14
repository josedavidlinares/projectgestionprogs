from django.contrib import admin
from .models import Categoria, Producto, Medio_Pago, Forma_Pago, Inventario, Historico_Precios, Ajuste_Stock

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Medio_Pago)
admin.site.register(Forma_Pago)
admin.site.register(Inventario)
admin.site.register(Historico_Precios)
admin.site.register(Ajuste_Stock)
