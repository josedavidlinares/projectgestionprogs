from django.urls import path
from . import views

urlpatterns = [
    path('cotizacion/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    # otras URLs de tu aplicación
    path('cotizacion/buscar_productos/', views.buscar_productos, name='buscar_productos'),
]
