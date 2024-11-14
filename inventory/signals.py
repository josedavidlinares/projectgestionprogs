# inventory/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Producto, Historico_Precios

@receiver(pre_save, sender=Producto)
def crear_historial_precio(sender, instance, **kwargs):
    # Verifica si el producto ya existe
    if instance.pk:
        producto = Producto.objects.get(pk=instance.pk)
        # Solo crea un historial si el precio_venta ha cambiado
        if instance.precio_venta != producto.precio_venta:
            Historico_Precios.objects.create(
                producto=instance,
                fecha_cambio=timezone.now().date(),
                precio=instance.precio_venta  # Usa el campo precio_venta
            )
            print(f"Historial creado para {instance.nombre} con precio {instance.precio_venta}")
        else:
            print(f"No se crea historial para {instance.nombre}, el precio no ha cambiado.")
