from django.test import TestCase
from accounts.models import T_Documento, Tipo_Usuario, Pais, Estado_Region, Municipio, Trabajador

class TrabajadorCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Configurando datos de prueba para Trabajador...")
        T_Documento.objects.create(nombre="Cédula", descripcion="Cédula de ciudadanía")
        
        tipo_usuario = Tipo_Usuario.objects.create(nombre="Admin", descripcion="Administrador del sistema")
        
        pais = Pais.objects.create(nombre="Colombia")
        estado = Estado_Region.objects.create(nombre="Cundinamarca", pais=pais)
        municipio = Municipio.objects.create(nombre="Bogotá", estado=estado)
        
        cls.municipio = municipio
        cls.tipo_usuario = tipo_usuario
        print(f"Datos de prueba configurados: Municipio {municipio.nombre}, Estado {estado.nombre}, País {pais.nombre}, Tipo Usuario {tipo_usuario.nombre}")

    def test_crear_trabajador(self):
        print("Creando un trabajador de prueba...")
        tipo_documento = T_Documento.objects.get(nombre="Cédula")
        
        trabajador = Trabajador.objects.create(
            tipo_documento=tipo_documento,
            documento_trabajador="111223344",
            nombre="Trabajador 1",
            apellido="Apellido Trabajador",
            email="trabajador1@example.com",
            telefono="3007654321",
            municipio=self.municipio,
            direccion="Carrera 50 #10-20, Bogotá",
            tipo_usuario=self.tipo_usuario
        )
        
        print(f"Trabajador creado: {trabajador.nombre}")
        self.assertEqual(trabajador.nombre, "Trabajador 1")
        self.assertEqual(trabajador.email, "trabajador1@example.com")

    def test_editar_trabajador(self):
        print("Editando un trabajador de prueba...")
        trabajador = Trabajador.objects.create(
            tipo_documento=T_Documento.objects.get(nombre="Cédula"),
            documento_trabajador="111223344",
            nombre="Trabajador 1",
            apellido="Apellido Trabajador",
            email="trabajador1@example.com",
            telefono="3007654321",
            municipio=self.municipio,
            direccion="Carrera 50 #10-20, Bogotá",
            tipo_usuario=self.tipo_usuario
        )
        
        trabajador.nombre = "Trabajador Editado"
        trabajador.email = "trabajadoreditado@example.com"
        trabajador.save()
        
        trabajador.refresh_from_db()
        print(f"Trabajador editado: {trabajador.nombre}")
        self.assertEqual(trabajador.nombre, "Trabajador Editado")
        self.assertEqual(trabajador.email, "trabajadoreditado@example.com")

    def test_eliminar_trabajador(self):
        print("Eliminando un trabajador de prueba...")
        trabajador = Trabajador.objects.create(
            tipo_documento=T_Documento.objects.get(nombre="Cédula"),
            documento_trabajador="111223344",
            nombre="Trabajador 1",
            apellido="Apellido Trabajador",
            email="trabajador1@example.com",
            telefono="3007654321",
            municipio=self.municipio,
            direccion="Carrera 50 #10-20, Bogotá",
            tipo_usuario=self.tipo_usuario
        )
        
        trabajador_id = trabajador.id
        trabajador.delete()
        print(f"Trabajador eliminado con ID: {trabajador_id}")
        with self.assertRaises(Trabajador.DoesNotExist):
            Trabajador.objects.get(id=trabajador_id)
