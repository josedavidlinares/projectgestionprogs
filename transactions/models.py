import datetime
from django.db import models
from accounts.models import Cliente, Trabajador
from inventory.models import Producto, Medio_Pago, Forma_Pago
from django.core.exceptions import ValidationError

class Cotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    estado = models.CharField(max_length=50, choices=[('activa', 'Activa'), ('inactiva', 'Inactiva')], default='activa')
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Añadimos este campo

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generate_unique_code('COT')
        super().save(*args, **kwargs)

    def generate_unique_code(self, prefix):
        year_suffix = datetime.datetime.now().year % 100
        last_code = Cotizacion.objects.filter(codigo__startswith=f"{prefix}-").order_by('codigo').last()
        if not last_code:
            new_code = f"{prefix}-000001-{year_suffix}"
        else:
            last_number = int(last_code.codigo.split('-')[1])
            new_code = f"{prefix}-{last_number + 1:06d}-{year_suffix}"
        return new_code

    def __str__(self):
        return f"Cotización {self.codigo} - {self.cliente.nombre}"

class Detalles_Cotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0')
        if self.precio_unitario <= 0:
            raise ValidationError('El precio unitario debe ser mayor a 0')

    def __str__(self):
        return f"Detalle Cotización {self.cotizacion.codigo} - {self.producto.nombre}"

#--------------------------------------------------------------------------------------------#

class Proforma(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    medio_pago = models.ForeignKey(Medio_Pago, on_delete=models.CASCADE)
    forma_pago = models.ForeignKey(Forma_Pago, on_delete=models.CASCADE)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)  # Fecha de vencimiento
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Campo porcentaje_iva
    estado = models.CharField(max_length=50, default='Pendiente', choices=[('Pendiente', 'Pendiente'), ('Pagado', 'Pagado'), ('Vencido', 'Vencido')])  # Estado
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    total_adeudado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_restante = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generate_unique_code('PROF')
        if self.saldo_restante <= 0:
            self.estado = 'Pagado'
        elif self.fecha_vencimiento and self.fecha_vencimiento < datetime.date.today():
            self.estado = 'Vencido'
        else:
            self.estado = 'Pendiente'
        super().save(*args, **kwargs)

    def generate_unique_code(self, prefix):
        year_suffix = datetime.datetime.now().year % 100
        last_code = Proforma.objects.filter(codigo__startswith(f"{prefix}-")).order_by('codigo').last()
        if not last_code:
            new_code = f"{prefix}-000001-{year_suffix}"
        else:
            last_number = int(last_code.codigo.split('-')[1])
            new_code = f"{prefix}-{last_number + 1:06d}-{year_suffix}"
        return new_code

    def __str__(self):
        return f"Proforma {self.codigo} - {self.cliente.nombre}"


class Detalles_Proforma(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal_prodProf = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0')
        if self.precio_unitario <= 0:
            raise ValidationError('El precio unitario debe ser mayor a 0')

    def __str__(self):
        return f"Detalle Proforma {self.proforma.codigo} - {self.producto.nombre}"

class PagoCredito(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateField(auto_now_add=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.proforma.saldo_restante -= self.monto_pagado
        self.proforma.save()

    def __str__(self):
        return f"Pago {self.id} - Proforma {self.proforma.codigo} - {self.monto_pagado}"
