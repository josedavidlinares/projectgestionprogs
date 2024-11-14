from django.urls import path
from . import views

urlpatterns = [
    # URLs para Categoria
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('categoria/editar/<int:id_categoria>/', views.editar_categoria, name='editar_categoria'),
    path('categoria/eliminar/<int:id_categoria>/', views.eliminar_categoria, name='eliminar_categoria'),

    # URLs para Medio de Pago
    path('medio_pago/crear/', views.crear_medio_pago, name='crear_medio_pago'),
    path('medio_pago/editar/<int:id_medio_pago>/', views.editar_medio_pago, name='editar_medio_pago'),
    path('medio_pago/eliminar/<int:id_medio_pago>/', views.eliminar_medio_pago, name='eliminar_medio_pago'),

    # URLs para Forma de Pago
    path('forma_pago/crear/', views.crear_forma_pago, name='crear_forma_pago'),
    path('forma_pago/editar/<int:id_forma_pago>/', views.editar_forma_pago, name='editar_forma_pago'),
    path('forma_pago/eliminar/<int:id_forma_pago>/', views.eliminar_forma_pago, name='eliminar_forma_pago'),


    # URL para Producto
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),

    # Historial Precios
    path('producto/historial/', views.historial_precio, name='historial_precio'),
        
]
