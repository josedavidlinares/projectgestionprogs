from django.db import models

class T_Contribuyente(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class T_Documento(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Estado_Region(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.pais}"

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado_Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre}, {self.estado}"

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    tipo_documento = models.ForeignKey(T_Documento, on_delete=models.CASCADE)
    documento_cliente = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    contribuyente = models.ForeignKey(T_Contribuyente, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    documento_proveedor = models.CharField(max_length=20, unique=True)
    tipo_documento = models.ForeignKey(T_Documento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    contribuyente = models.ForeignKey(T_Contribuyente, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    documento_trabajador = models.CharField(max_length=20)
    tipo_documento = models.ForeignKey(T_Documento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    tipo_usuario = models.ForeignKey('Tipo_Usuario', on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Tipo_Usuario(models.Model):
    id = models.AutoField(primary_key=True)  # Usamos "id" como campo primario
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre
