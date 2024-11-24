from django.urls import path
from . import views

urlpatterns = [
    path('cotizacion/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    # otras URLs de tu aplicación
    path('cotizacion/buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('cotizacion/listar/', views.listar_cotizaciones, name='listar_cotizaciones'),
    path('cotizacion/editar/<int:cotizacion_id>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizacion/eliminar/<int:cotizacion_id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
]
