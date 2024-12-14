from django.urls import path
from . import views

urlpatterns = [
    # URLS para las Cotizaciones
    path('cotizacion/crear/', views.crear_cotizacion, name='crear_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/', views.detalle_cotizacion, name='detalle_cotizacion'),
    path('cotizacion/buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('cotizacion/listar/', views.listar_todas_las_cotizaciones, name='listar_todas_las_cotizaciones'),
    path('cotizacion/editar/<int:cotizacion_id>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/pdf/', views.generar_pdf_cotizacion, name='generar_pdf_cotizacion'),

    # URLS para las Proformas
    path('proforma/crear/', views.crear_proforma, name='crear_proforma'),
    path('proforma/<int:proforma_id>/', views.detalle_proforma, name='detalle_proforma'),
    path('proforma/<int:proforma_id>/registrar-pago/', views.registrar_pago, name='registrar_pago'),
    path('proforma/listar/', views.listar_todas_las_proformas, name='listar_todas_las_proformas'),
    path('proforma/<int:proforma_id>/pdf/', views.generar_pdf_proforma, name='generar_pdf_proforma'),

    # Otras URLS
    path('resumen-diario/', views.resumen_diario, name='resumen_diario'),
]
