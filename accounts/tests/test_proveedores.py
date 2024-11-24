from django.test import TestCase
from accounts.models import T_Documento, T_Contribuyente, Pais, Estado_Region, Municipio, Proveedor

class ProveedorCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Configurando datos de prueba para Proveedor...")
        T_Documento.objects.create(nombre="Cédula", descripcion="Cédula de ciudadanía")
        T_Contribuyente.objects.create(nombre="Contribuyente 1", descripcion="Contribuyente de prueba")
        
        pais = Pais.objects.create(nombre="Colombia")
        estado = Estado_Region.objects.create(nombre="Cundinamarca", pais=pais)
        municipio = Municipio.objects.create(nombre="Bogotá", estado=estado)
        
        cls.municipio = municipio
        print(f"Datos de prueba configurados: Municipio {municipio.nombre}, Estado {estado.nombre}, País {pais.nombre}")

    def test_crear_proveedor(self):
        print("Creando un proveedor de prueba...")
        tipo_documento = T_Documento.objects.get(nombre="Cédula")
        contribuyente = T_Contribuyente.objects.get(nombre="Contribuyente 1")
        
        proveedor = Proveedor.objects.create(
            tipo_documento=tipo_documento,
            documento_proveedor="123456789",
            nombre="Proveedor 1",
            contribuyente=contribuyente,
            email="proveedor1@example.com",
            telefono="3009876543",
            municipio=self.municipio,
            direccion="Carrera 45 #123-45, Bogotá"
        )
        
        print(f"Proveedor creado: {proveedor.nombre}")
        self.assertEqual(proveedor.nombre, "Proveedor 1")
        self.assertEqual(proveedor.email, "proveedor1@example.com")

    def test_editar_proveedor(self):
        print("Editando un proveedor de prueba...")
        proveedor = Proveedor.objects.create(
            tipo_documento=T_Documento.objects.get(nombre="Cédula"),
            documento_proveedor="123456789",
            nombre="Proveedor 1",
            contribuyente=T_Contribuyente.objects.get(nombre="Contribuyente 1"),
            email="proveedor1@example.com",
            telefono="3009876543",
            municipio=self.municipio,
            direccion="Carrera 45 #123-45, Bogotá"
        )
        
        proveedor.nombre = "Proveedor Editado"
        proveedor.email = "proveedoreditado@example.com"
        proveedor.save()
        
        proveedor.refresh_from_db()
        print(f"Proveedor editado: {proveedor.nombre}")
        self.assertEqual(proveedor.nombre, "Proveedor Editado")
        self.assertEqual(proveedor.email, "proveedoreditado@example.com")

    def test_eliminar_proveedor(self):
        print("Eliminando un proveedor de prueba...")
        proveedor = Proveedor.objects.create(
            tipo_documento=T_Documento.objects.get(nombre="Cédula"),
            documento_proveedor="123456789",
            nombre="Proveedor 1",
            contribuyente=T_Contribuyente.objects.get(nombre="Contribuyente 1"),
            email="proveedor1@example.com",
            telefono="3009876543",
            municipio=self.municipio,
            direccion="Carrera 45 #123-45, Bogotá"
        )
        
        proveedor_id = proveedor.id
        proveedor.delete()
        print(f"Proveedor eliminado con ID: {proveedor_id}")
        with self.assertRaises(Proveedor.DoesNotExist):
            Proveedor.objects.get(id=proveedor_id)
