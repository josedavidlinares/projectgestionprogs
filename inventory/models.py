from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    cod_producto = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    stock_min = models.IntegerField(default=0)
    stock_max = models.IntegerField(default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    mercancia_muerta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Medio_Pago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Forma_Pago(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    proveedor = models.ForeignKey('accounts.Proveedor', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    n_lote = models.CharField(max_length=50, blank=True, null=True)
    precio_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha}"

class Historico_Precios(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_cambio = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha_cambio}"

class Ajuste_Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=255)
    fecha = models.DateField()

    def __str__(self):
        return f"Ajuste {self.id} - {self.producto.nombre}"
