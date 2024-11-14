from django.urls import path
from . import views

urlpatterns = [
    # URLs para T_Contribuyente
    path('tcontribuyente/crear/', views.crear_t_contribuyente, name='crear_t_contribuyente'),
    path('tcontribuyente/editar/<int:id_tcont>/', views.editar_t_contribuyente, name='editar_t_contribuyente'),
    path('tcontribuyente/eliminar/<int:id_tcont>/', views.eliminar_t_contribuyente, name='eliminar_t_contribuyente'),

    # URLs para T_Documento
    path('tdocumento/crear/', views.crear_t_documento, name='crear_t_documento'),
    path('tdocumento/editar/<int:id_doc>/', views.editar_t_documento, name='editar_t_documento'),
    path('tdocumento/eliminar/<int:id_doc>/', views.eliminar_t_documento, name='eliminar_t_documento'),

    # URLs para Pais
    path('pais/crear/', views.crear_pais, name='crear_pais'),
    path('pais/editar/<int:id_pais>/', views.editar_pais, name='editar_pais'),
    path('pais/eliminar/<int:id_pais>/', views.eliminar_pais, name='eliminar_pais'),

    # URLs para Estado_Region
    path('estado_region/crear/', views.crear_estado_region, name='crear_estado_region'),
    path('estado_region/editar/<int:id_estado>/', views.editar_estado_region, name='editar_estado_region'),
    path('estado_region/eliminar/<int:id_estado>/', views.eliminar_estado_region, name='eliminar_estado_region'),
    path('obtener_paises/', views.obtener_paises, name='obtener_paises'),

    # URLs para Municipio
    path('municipio/crear/', views.crear_municipio, name='crear_municipio'),
    path('municipio/editar/<int:id_municipio>/', views.editar_municipio, name='editar_municipio'),
    path('municipio/eliminar/<int:id_municipio>/', views.eliminar_municipio, name='eliminar_municipio'),
    path('obtener_departamentos/', views.obtener_departamentos, name='obtener_departamentos'),
    
    # URLs para Cliente
    path('cliente/crear/', views.crear_cliente, name='crear_cliente'),
    path('cliente/editar/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),

    # URLs para Proveedor
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/editar/<int:id_proveedor>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedor/eliminar/<int:id_proveedor>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # URLs para Trabajador
    path('trabajador/crear/', views.crear_trabajador, name='crear_trabajador'),
    path('trabajador/editar/<int:id_trabajador>/', views.editar_trabajador, name='editar_trabajador'),
    path('trabajador/eliminar/<int:id_trabajador>/', views.eliminar_trabajador, name='eliminar_trabajador'),

    # URLs para Tipo_Usuario
    path('tipo_usuario/crear/', views.crear_tipo_usuario, name='crear_tipo_usuario'),
    path('tipo_usuario/editar/<int:id>/', views.editar_tipo_usuario, name='editar_tipo_usuario'),
    path('tipo_usuario/eliminar/<int:id>/', views.eliminar_tipo_usuario, name='eliminar_tipo_usuario'),

]
