from django.db import models
from accounts.models import Cliente, Trabajador
from inventory.models import Producto

class Cotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, default='Activo')

    def __str__(self):
        return f"Cotización {self.id} - {self.cliente.nombre}"

class Detalles_Cotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal_prodC = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Cotización {self.cotizacion.id} - {self.producto.nombre}"

class Proforma(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    medio_pago = models.ForeignKey('inventory.Medio_Pago', on_delete=models.CASCADE)
    forma_pago = models.ForeignKey('inventory.Forma_Pago', on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, default='Activo')

    def __str__(self):
        return f"Proforma {self.id} - {self.cliente.nombre}"

class Detalles_Proforma(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal_prodProf = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Proforma {self.proforma.id} - {self.producto.nombre}"
