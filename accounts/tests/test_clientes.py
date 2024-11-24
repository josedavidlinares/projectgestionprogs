from django.test import TestCase
from accounts.models import T_Documento, T_Contribuyente, Pais, Estado_Region, Municipio, Cliente

class ClienteCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Configurando datos de prueba para Cliente...")
        # Crear tipos de documento de prueba
        T_Documento.objects.create(nombre="Cédula", descripcion="Cédula de ciudadanía")
        
        # Crear contribuyentes de prueba
        T_Contribuyente.objects.create(nombre="Contribuyente 1", descripcion="Contribuyente de prueba")
        
        # Crear países, estados y municipios de prueba
        pais = Pais.objects.create(nombre="Colombia")
        estado = Estado_Region.objects.create(nombre="Cundinamarca", pais=pais)
        municipio = Municipio.objects.create(nombre="Bogotá", estado=estado)
        
        # Guardamos los datos relacionados para usarlos en los tests
        cls.municipio = municipio
        print(f"Datos de prueba configurados: Municipio {municipio.nombre}, Estado {estado.nombre}, País {pais.nombre}")

    def test_crear_cliente(self):
        print("Creando un cliente de prueba...")
        # Crear cliente de prueba
        tipo_documento = T_Documento.objects.get(nombre="Cédula")
        contribuyente = T_Contribuyente.objects.get(nombre="Contribuyente 1")
        
        cliente = Cliente.objects.create(
            tipo_documento=tipo_documento,
            documento_cliente="987654321",
            nombre="Cliente 1",
            apellido="Apellido 1",
            contribuyente=contribuyente,
            email="cliente1@example.com",
            telefono="3001234567",
            municipio=self.municipio,
            direccion="Carrera 10 #22-33, Bogotá"
        )
        
        # Verificar creación
        print(f"Cliente creado: {cliente.nombre}")
        self.assertEqual(cliente.nombre, "Cliente 1")
        self.assertEqual(cliente.email, "cliente1@example.com")

    def test_editar_cliente(self):
        print("Editando un cliente de prueba...")
        cliente = Cliente.objects.create(
            tipo_documento=T_Documento.objects.get(nombre="Cédula"),
            documento_cliente="987654321",
            nombre="Cliente 1",
            apellido="Apellido 1",
            contribuyente=T_Contribuyente.objects.get(nombre="Contribuyente 1"),
            email="cliente1@example.com",
            telefono="3001234567",
            municipio=self.municipio,
            direccion="Carrera 10 #22-33, Bogotá"
        )
        
        # Editamos el cliente
        cliente.nombre = "Cliente Editado"
        cliente.email = "clienteeditado@example.com"
        cliente.save()
        
        cliente.refresh_from_db()
        print(f"Cliente editado: {cliente.nombre}")
        self.assertEqual(cliente.nombre, "Cliente Editado")
        self.assertEqual(cliente.email, "clienteeditado@example.com")

    def test_eliminar_cliente(self):
        print("Eliminando un cliente de prueba...")
        cliente = Cliente.objects.create(
            tipo_documento=T_Documento.objects.get(nombre="Cédula"),
            documento_cliente="987654321",
            nombre="Cliente 1",
            apellido="Apellido 1",
            contribuyente=T_Contribuyente.objects.get(nombre="Contribuyente 1"),
            email="cliente1@example.com",
            telefono="3001234567",
            municipio=self.municipio,
            direccion="Carrera 10 #22-33, Bogotá"
        )
        
        cliente_id = cliente.id
        cliente.delete()
        print(f"Cliente eliminado con ID: {cliente_id}")
        with self.assertRaises(Cliente.DoesNotExist):
            Cliente.objects.get(id=cliente_id)
