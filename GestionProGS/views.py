from django.shortcuts import render
from transactions.models import Proforma, Cotizacion, Detalles_Proforma
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    
    # Obtener proformas y cotizaciones del día, limitando a las 5 más recientes
    proformas_hoy = Proforma.objects.filter(
        fecha_emision__year=hoy.year,
        fecha_emision__month=hoy.month,
        fecha_emision__day=hoy.day
    ).order_by('-fecha_emision')[:5]
    
    cotizaciones_hoy = Cotizacion.objects.filter(
        fecha_emision__year=hoy.year,
        fecha_emision__month=hoy.month,
        fecha_emision__day=hoy.day
    ).order_by('-fecha_emision')[:5]
    
    proformas_detalles = []
    total_dinero_ventas = 0

    for proforma in proformas_hoy:
        detalles = Detalles_Proforma.objects.filter(proforma=proforma)
        
        subtotal_incluyendo_iva = sum(detalle.subtotal_prodProf for detalle in detalles)
        porcentaje_iva = proforma.porcentaje_iva / 100
        total_iva = subtotal_incluyendo_iva * (porcentaje_iva / (1 + porcentaje_iva))
        subtotal = subtotal_incluyendo_iva - total_iva
        porcentaje_descuento = proforma.descuento / 100
        descuento = subtotal * porcentaje_descuento
        subtotal_con_descuento = subtotal - descuento
        total = subtotal_incluyendo_iva
        total_dinero_ventas += total
        
        proformas_detalles.append({
            'proforma': proforma,
            'total_subtotal': subtotal,
            'total_iva': total_iva,
            'descuento': descuento,
            'total': total,
            'total_cantidad': sum(detalle.cantidad for detalle in detalles),
            'tipo_documento': proforma.cliente.tipo_documento.nombre,
            'numero_documento': proforma.cliente.documento_cliente,
        })
    
    total_ventas = len(proformas_hoy)  # Contar el total de ventas del día actual
    
    context = {
        'proformas_detalles': proformas_detalles,
        'cotizaciones_hoy': cotizaciones_hoy,
        'total_ventas': total_ventas,
        'total_dinero_ventas': total_dinero_ventas,
        'hoy': hoy,
    }
    
    return render(request, 'dashboard.html', context)


def index(request):
    # Lógica para preparar datos para la página de inicio
    context = {}  # Contexto para pasar datos a la plantilla
    return render(request, 'index.html', context)
