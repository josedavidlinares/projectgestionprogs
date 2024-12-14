from django.shortcuts import render, redirect, get_object_or_404
from .forms import CotizacionForm, DetallesCotizacionForm, DetallesCotizacionFormSet, ProformaForm, DetallesProformaForm
from .models import Cotizacion, Detalles_Cotizacion, Producto, Proforma, Detalles_Proforma, PagoCredito
from accounts.models import Cliente
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from decimal import Decimal
from django.core.paginator import Paginator 
from django.db.models import Q
import datetime
import json
from django.contrib.auth.decorators import login_required


def generar_codigo_cotizacion():
    prefix = "COT"
    year_suffix = datetime.datetime.now().year % 100
    last_code = Cotizacion.objects.filter(codigo__startswith=f"{prefix}-").order_by('codigo').last()
    if not last_code:
        new_code = f"{prefix}-000001-{year_suffix}"
    else:
        last_number = int(last_code.codigo.split('-')[1])
        new_code = f"{prefix}-{last_number + 1:06d}-{year_suffix}"
    return new_code

@login_required
def crear_cotizacion(request):
    try:
        codigo = generar_codigo_cotizacion()
        cotizacion = None
        detalles = []

        if request.method == 'POST':
            cotizacion_form = CotizacionForm(request.POST)
            
            # Obtener los productos enviados por la tupla
            productos_json = request.POST.get('productos_json', '[]')
            try:
                productos_list = json.loads(productos_json)
            except json.JSONDecodeError:
                productos_list = []

            if cotizacion_form.is_valid():
                cotizacion = cotizacion_form.save(commit=False)
                cotizacion.codigo = codigo  # Asignar el código generado para la nueva cotización
                cotizacion.save()

                # Guardar los detalles de la cotización
                for producto in productos_list:
                    detalle = Detalles_Cotizacion(
                        cotizacion=cotizacion,
                        producto_id=producto['id'],
                        cantidad=Decimal(producto['cantidad']),
                        precio_unitario=Decimal(producto['precio']),
                        subtotal=Decimal(producto['subtotal'])
                    )
                    detalle.save()

                return redirect('listar_todas_las_cotizaciones')
            else:
                messages.error(request, "Error en el formulario de cotización. Por favor, verifica los datos ingresados.")
        else:
            cotizacion_form = CotizacionForm()

        return render(request, 'transactions/cotizacion.html', {
            'form': cotizacion_form,
            'cotizacion': cotizacion,
            'productos_list': detalles,
            'codigo': codigo  # Pasar el código al template
        })
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en crear_cotizacion: {e}")
        messages.error(request, "Hubo un problema al cargar el formulario. Por favor, intenta de nuevo más tarde.")
        return render(request, 'transactions/error.html', {'error': str(e)})


@login_required
def editar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)
    detalles = Detalles_Cotizacion.objects.filter(cotizacion=cotizacion)
    codigo = cotizacion.codigo

    if request.method == 'POST':
        cotizacion_form = CotizacionForm(request.POST, instance=cotizacion)
        
        # Obtener los productos enviados por la tupla
        productos_json = request.POST.get('productos_json', '[]')
        try:
            productos_list = json.loads(productos_json)
        except json.JSONDecodeError:
            productos_list = []

        # Imprimir los productos recibidos
        print("Productos recibidos:")
        for producto in productos_list:
            print(f"ID: {producto['id']}, Código: {producto['codigo']}, Nombre: {producto['nombre']}, Precio: {producto['precio']}, Cantidad: {producto['cantidad']}, Subtotal: {producto['subtotal']}")

        if cotizacion_form.is_valid():
            cotizacion = cotizacion_form.save(commit=False)
            cotizacion.save()
            print(f"Cotización guardada con ID: {cotizacion.id}")

            # Crear un conjunto de los ids de los productos en la solicitud
            productos_ids = set(producto['id'] for producto in productos_list)

            # Eliminar los detalles que ya no están en la solicitud
            detalles.exclude(producto_id__in=productos_ids).delete()

            # Actualizar o crear los detalles existentes
            for producto in productos_list:
                detalle, created = Detalles_Cotizacion.objects.update_or_create(
                    cotizacion=cotizacion,
                    producto_id=producto['id'],
                    defaults={
                        'cantidad': Decimal(producto['cantidad']),
                        'precio_unitario': Decimal(producto['precio']),
                        'subtotal': Decimal(producto['subtotal'])
                    }
                )
                if created:
                    print(f"Detalle creado para producto ID: {producto['id']}")
                else:
                    print(f"Detalle actualizado para producto ID: {producto['id']}")

            return redirect('listar_todas_las_cotizaciones')
        else:
            print(f"Errores en el formulario de cotización: {cotizacion_form.errors.as_json()}")
            messages.error(request, "Error en el formulario de cotización")
    else:
        cotizacion_form = CotizacionForm(instance=cotizacion)

    productos_list = []
    for i, detalle in enumerate(detalles):
        productos_list.append({
            'id': detalle.producto.id,
            'codigo': detalle.producto.cod_producto,
            'nombre': detalle.producto.nombre,
            'precio': float(detalle.precio_unitario),  # Asegurar que el precio es correcto
            'cantidad': detalle.cantidad,
        })

    # Eliminar duplicados basados en el id del producto
    productos_list_filtrados = []
    seen_ids = set()
    for producto in productos_list:
        if producto['id'] not in seen_ids:
            productos_list_filtrados.append(producto)
            seen_ids.add(producto['id'])

    return render(request, 'transactions/cotizacion.html', {
        'form': cotizacion_form,
        'cotizacion': cotizacion,
        'productos_list': productos_list_filtrados,
        'codigo': codigo  # Pasar el código al template
    })


@login_required
def buscar_productos(request):
    try:
        query = request.GET.get('q', '')

        if not query:
            return JsonResponse({'error': 'No se proporcionó una consulta de búsqueda.'}, status=400)

        productos = Producto.objects.filter(nombre__icontains=query)
        productos_list = [{
            'id': producto.id,
            'codigo': producto.cod_producto,
            'nombre': producto.nombre,
            'precio': producto.precio_venta,
            'stock': producto.stock,
        } for producto in productos]

        print(productos_list)
        return JsonResponse({'productos': productos_list})
    except ObjectDoesNotExist as e:
        print("Error: Producto no encontrado:", e)
        return JsonResponse({'error': 'Producto no encontrado.'}, status=404)
    except Exception as e:
        print("Error en buscar_productos:", e)
        print(traceback.format_exc())
        return JsonResponse({'error': 'Ocurrió un error en el servidor.'}, status=500)

@login_required
def listar_todas_las_cotizaciones(request):
    print("Vista listar_todas_las_cotizaciones llamada")
    
    buscar = request.GET.get('buscar', '')
    page_number = request.GET.get('page', 1)
    print(f"Buscar: {buscar}, Página: {page_number}")

    cotizaciones = Cotizacion.objects.filter(
        Q(codigo__icontains=buscar) |
        Q(cliente__nombre__icontains=buscar) |
        Q(fecha_emision__icontains=buscar)
    ).order_by('fecha_emision')  # Ordenamos por fecha de emisión

    paginator = Paginator(cotizaciones, 10)  # Mostramos 10 cotizaciones por página
    paginated_cotizaciones = paginator.get_page(page_number)
    print(f"Total cotizaciones: {paginator.count}")

    cotizaciones_detalles = []

    for cotizacion in paginated_cotizaciones:
        print(f"Procesando cotización: {cotizacion.codigo}, Cliente: {cotizacion.cliente.nombre}, Fecha de Emisión: {cotizacion.fecha_emision}, Fecha de Vencimiento: {cotizacion.fecha_vencimiento}, Estado: {cotizacion.estado}")
        detalles = Detalles_Cotizacion.objects.filter(cotizacion=cotizacion)
        
        subtotal_incluyendo_iva = sum(detalle.subtotal for detalle in detalles)
        porcentaje_iva = cotizacion.porcentaje_iva / 100
        total_iva = subtotal_incluyendo_iva * (porcentaje_iva / (1 + porcentaje_iva))
        subtotal = subtotal_incluyendo_iva - total_iva
        porcentaje_descuento = cotizacion.descuento / 100
        descuento = subtotal * porcentaje_descuento
        subtotal_con_descuento = subtotal - descuento
        total = subtotal_con_descuento + total_iva
        total_cantidad = sum(detalle.cantidad for detalle in detalles)
        
        print(f"Total Subtotal: {subtotal}, Total IVA: {total_iva}, Descuento: {descuento}, Total: {total}, Total Cantidad: {total_cantidad}")
        
        cotizaciones_detalles.append({
            'cotizacion': cotizacion,
            'total_subtotal': subtotal,
            'total_iva': total_iva,
            'descuento': descuento,
            'total': total,
            'total_cantidad': total_cantidad,
            'tipo_documento': cotizacion.cliente.tipo_documento,
            'numero_documento': cotizacion.cliente.documento_cliente,
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Solicitud AJAX detectada")
        cotizaciones_json = [
            {
                'id': cotizacion['cotizacion'].pk,
                'codigo': cotizacion['cotizacion'].codigo,
                'cliente': cotizacion['cotizacion'].cliente.nombre,
                'tipo_documento': cotizacion['cotizacion'].cliente.tipo_documento,
                'numero_documento': cotizacion['cotizacion'].cliente.documento_cliente,
                'fecha_emision': cotizacion['cotizacion'].fecha_emision.strftime('%Y-%m-%d'),
                'fecha_vencimiento': cotizacion['cotizacion'].fecha_vencimiento.strftime('%Y-%m-%d'),
                'estado': cotizacion['cotizacion'].estado,
                'total_cantidad': cotizacion['total_cantidad'],
                'total_subtotal': cotizacion['total_subtotal'],
                'total_iva': cotizacion['total_iva'],
                'descuento': cotizacion['descuento'],
                'total_factura': cotizacion['total'],
            }
            for cotizacion in cotizaciones_detalles
        ]
        print("Enviando JSON con las cotizaciones: ", cotizaciones_json)
        return JsonResponse({'cotizaciones': cotizaciones_json})

    context = {
        'cotizaciones_detalles': cotizaciones_detalles,
        'paginated_cotizaciones': paginated_cotizaciones,  # Añadir los datos de paginación al contexto
    }
    print("Renderizando template con context: ", context)
    return render(request, 'transactions/listar_cotizaciones.html', context)

@login_required
def detalle_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    detalles_cotizacion = Detalles_Cotizacion.objects.filter(cotizacion=cotizacion)

    subtotal_incluyendo_iva = sum(detalle.subtotal for detalle in detalles_cotizacion)
    porcentaje_iva = cotizacion.porcentaje_iva / 100
    total_iva = subtotal_incluyendo_iva * (porcentaje_iva / (1 + porcentaje_iva))
    subtotal = subtotal_incluyendo_iva - total_iva
    porcentaje_descuento = cotizacion.descuento / 100
    descuento = subtotal * porcentaje_descuento
    subtotal_con_descuento = subtotal - descuento
    total = subtotal_con_descuento + total_iva

    context = {
        'cotizacion': cotizacion,
        'detalles_cotizacion': detalles_cotizacion,
        'subtotal': subtotal,
        'total_iva': total_iva,
        'descuento': descuento,
        'total': total,
        'tipo_documento': cotizacion.cliente.tipo_documento,
        'numero_documento': cotizacion.cliente.documento_cliente,
    }
    return render(request, 'transactions/detalle_cotizacion.html', context)

import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from .models import Cotizacion, Detalles_Cotizacion

def generar_pdf_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    detalles_cotizacion = Detalles_Cotizacion.objects.filter(cotizacion=cotizacion)

    subtotal_incluyendo_iva = sum(detalle.subtotal for detalle in detalles_cotizacion)
    porcentaje_iva = cotizacion.porcentaje_iva / 100
    subtotal = subtotal_incluyendo_iva / (1 + porcentaje_iva)
    total_iva = subtotal_incluyendo_iva - subtotal

    context = {
        'cotizacion': cotizacion,
        'detalles_cotizacion': detalles_cotizacion,
        'subtotal': subtotal,
        'total_iva': total_iva,
        'tipo_documento': cotizacion.cliente.tipo_documento.nombre,
        'numero_documento': cotizacion.cliente.documento_cliente,
    }

    html_string = render_to_string('transactions/detalle_cotizacion.html', context)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        'page-size': 'A4',  # Establecer el tamaño de la página
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'load-error-handling': 'ignore',
        'no-stop-slow-scripts': '',
        'debug-javascript': '',
        'enable-local-file-access': '',
        'zoom': '1.25',  # Ajustar zoom si es necesario
    }
    pdf = pdfkit.from_string(html_string, False, configuration=config, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion_{cotizacion.codigo}.pdf"'

    return response


#-------------------------------------------------------------------------------------------------------------

def generar_codigo_proforma():
    prefix = "PROF"
    year_suffix = datetime.datetime.now().year % 100
    last_code = Proforma.objects.filter(codigo__startswith=f"{prefix}-").order_by('codigo').last()
    if not last_code:
        new_code = f"{prefix}-000001-{year_suffix}"
    else:
        last_number = int(last_code.codigo.split('-')[1])
        new_code = f"{prefix}-{last_number + 1:06d}-{year_suffix}"
    return new_code

@login_required
def crear_proforma(request):
    codigo = generar_codigo_proforma()
    proforma = None
    detalles = []

    if request.method == 'POST':
        proforma_form = ProformaForm(request.POST)
        
        # Obtener los productos enviados por la tupla
        productos_json = request.POST.get('productos_json', '[]')
        try:
            productos_list = json.loads(productos_json)
        except json.JSONDecodeError:
            productos_list = []

        # Imprimir todos los datos recibidos
        print("Datos del formulario de proforma:")
        print(f"Cliente: {request.POST.get('cliente')}")
        print(f"Trabajador: {request.POST.get('trabajador')}")
        print(f"Medio de Pago: {request.POST.get('medio_pago')}")
        print(f"Forma de Pago (oculto): Contado")
        print(f"Fecha de Emisión: {request.POST.get('fecha_emision')}")
        print(f"Fecha de Vencimiento: {request.POST.get('fecha_vencimiento')}")
        print(f"Descuento: {request.POST.get('descuento')}")
        print(f"Porcentaje IVA: {request.POST.get('porcentaje_iva')}")
        print(f"Estado (oculto): Pagado")

        # Imprimir los productos recibidos
        print("Productos recibidos:")
        for producto in productos_list:
            print(f"ID: {producto['id']}, Código: {producto['codigo']}, Nombre: {producto['nombre']}, Precio: {producto['precio']}, Cantidad: {producto['cantidad']}, Subtotal: {producto['subtotal']}")

        if proforma_form.is_valid():
            proforma = proforma_form.save(commit=False)
            proforma.codigo = codigo  # Asignar el código generado para la nueva proforma
            proforma.medio_pago_id = 1  # Forma de pago "Contado" con id 3
            proforma.forma_pago_id = 1  # ID de forma de pago "Contado"
            subtotal = sum(Decimal(p['subtotal']) for p in productos_list)
            porcentaje_iva = Decimal(proforma_form.cleaned_data['porcentaje_iva']) / 100
            total_iva = subtotal * porcentaje_iva
            proforma.total_adeudado = subtotal + total_iva - proforma.descuento
            proforma.total_pagado = proforma.total_adeudado
            proforma.saldo_restante = 0
            proforma.estado = 'Pagado'
            proforma.save()
            print(f"Proforma guardada con ID: {proforma.id}")

            # Guardar los detalles de la proforma
            for producto in productos_list:
                detalle = Detalles_Proforma(
                    proforma=proforma,
                    producto_id=producto['id'],
                    cantidad=Decimal(producto['cantidad']),
                    precio_unitario=Decimal(producto['precio']),
                    subtotal_prodProf=Decimal(producto['subtotal'])
                )
                detalle.save()

            return redirect('listar_todas_las_cotizaciones')
        else:
            print(f"Errores en el formulario de proforma: {proforma_form.errors.as_json()}")
            messages.error(request, "Error en el formulario de proforma")
    else:
        proforma_form = ProformaForm()

    return render(request, 'transactions/proforma.html', {
        'form': proforma_form,
        'proforma': proforma,
        'productos_list': detalles,
        'codigo': codigo  # Pasar el código al template
    })

from django.shortcuts import get_object_or_404
from .models import Proforma, Detalles_Proforma

@login_required
def detalle_proforma(request, proforma_id):
    proforma = get_object_or_404(Proforma, id=proforma_id)
    detalles_factura = Detalles_Proforma.objects.filter(proforma=proforma)

    # Calcula el subtotal incluyendo IVA
    subtotal_incluyendo_iva = sum(detalle.subtotal_prodProf for detalle in detalles_factura)

    # Calcula el porcentaje de IVA y el total de IVA
    porcentaje_iva = proforma.porcentaje_iva / 100
    total_iva = subtotal_incluyendo_iva * (porcentaje_iva / (1 + porcentaje_iva))

    # Calcula el subtotal sin IVA
    subtotal = subtotal_incluyendo_iva - total_iva

    # Calcula el porcentaje de descuento y el total de descuento
    porcentaje_descuento = proforma.descuento / 100
    descuento = subtotal * porcentaje_descuento

    # Calcula el subtotal con descuento
    subtotal_con_descuento = subtotal - descuento

    # Calcula el total de la factura
    total = subtotal_con_descuento + total_iva

    context = {
        'factura': proforma,
        'detalles_factura': detalles_factura,
        'subtotal': subtotal,
        'total_iva': total_iva,
        'descuento': descuento,
        'total': total,
        'tipo_documento': proforma.cliente.tipo_documento.nombre,
        'numero_documento': proforma.cliente.documento_cliente,
    }
    return render(request, 'transactions/detalle_proforma.html', context)

@login_required
def registrar_pago(request, proforma_id):
    proforma = get_object_or_404(Proforma, id=proforma_id)
    if request.method == 'POST':
        form = PagoCreditoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.proforma = proforma
            pago.save()
            proforma.total_pagado += pago.monto_pagado
            proforma.saldo_restante -= pago.monto_pagado
            if proforma.saldo_restante <= 0:
                proforma.estado = 'Pagado'
            proforma.save()
            return redirect('detalle_proforma', proforma_id=proforma.id)
    else:
        form = PagoCreditoForm()
    return render(request, 'transactions/registrar_pago.html', {'form': form, 'proforma': proforma})

@login_required
def resumen_diario(request):
    hoy = datetime.datetime.now().date()
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
    else:
        fecha_inicio = hoy
        fecha_fin = hoy
    
    proformas = Proforma.objects.filter(fecha_emision__range=(fecha_inicio, fecha_fin))
    total_facturado = proformas.aggregate(total=Sum('total_iva'))['total'] or 0
    
    pagos = PagoCredito.objects.filter(fecha_pago__range=(fecha_inicio, fecha_fin))
    total_pagado = pagos.aggregate(total=Sum('monto_pagado'))['total'] or 0
    
    return render(request, 'transactions/resumen_diario.html', {
        'proformas': proformas,
        'total_facturado': total_facturado,
        'pagos': pagos,
        'total_pagado': total_pagado,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })

@login_required
def listar_todas_las_proformas(request):
    
    buscar = request.GET.get('buscar', '')
    page_number = request.GET.get('page', 1)

    proformas = Proforma.objects.filter(
        Q(codigo__icontains=buscar) |
        Q(cliente__nombre__icontains=buscar) |
        Q(fecha_emision__icontains=buscar)
    ).order_by('fecha_emision')  # Ordenamos por fecha de emisión

    paginator = Paginator(proformas, 10)  # Mostramos 10 proformas por página
    paginated_proformas = paginator.get_page(page_number)

    proformas_detalles = []

    for proforma in paginated_proformas:
        detalles = Detalles_Proforma.objects.filter(proforma=proforma)
        
        subtotal_incluyendo_iva = sum(detalle.subtotal_prodProf for detalle in detalles)
        porcentaje_iva = proforma.porcentaje_iva / 100
        total_iva = subtotal_incluyendo_iva * (porcentaje_iva / (1 + porcentaje_iva))
        subtotal = subtotal_incluyendo_iva - total_iva
        porcentaje_descuento = proforma.descuento / 100
        descuento = subtotal * porcentaje_descuento
        subtotal_con_descuento = subtotal - descuento
        total = subtotal_con_descuento + total_iva
        total_cantidad = sum(detalle.cantidad for detalle in detalles)
        
        
        proformas_detalles.append({
            'proforma': proforma,
            'total_subtotal': subtotal,
            'total_iva': total_iva,
            'descuento': descuento,
            'total': total,
            'total_cantidad': total_cantidad,
            'tipo_documento': proforma.cliente.tipo_documento.nombre,
            'numero_documento': proforma.cliente.documento_cliente,
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        proformas_json = [
            {
                'id': proforma['proforma'].pk,
                'codigo': proforma['proforma'].codigo,
                'cliente': proforma['proforma'].cliente.nombre,
                'tipo_documento': proforma['proforma'].cliente.tipo_documento.nombre,
                'numero_documento': proforma['proforma'].cliente.documento_cliente,
                'fecha_emision': proforma['proforma'].fecha_emision.strftime('%Y-%m-%d'),
                'fecha_vencimiento': proforma['proforma'].fecha_vencimiento.strftime('%Y-%m-%d'),
                'estado': proforma['proforma'].estado,
                'total_cantidad': proforma['total_cantidad'],
                'total_subtotal': proforma['total_subtotal'],
                'total_iva': proforma['total_iva'],
                'descuento': proforma['descuento'],
                'total_factura': proforma['total'],
            }
            for proforma in proformas_detalles
        ]
        return JsonResponse({'proformas': proformas_json})

    context = {
        'proformas_detalles': proformas_detalles,
        'paginated_proformas': paginated_proformas,  # Añadir los datos de paginación al contexto
    }
    return render(request, 'transactions/listar_proformas.html', context)


import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from .models import Proforma, Detalles_Proforma

def generar_pdf_proforma(request, proforma_id):
    proforma = get_object_or_404(Proforma, id=proforma_id)
    detalles_factura = Detalles_Proforma.objects.filter(proforma=proforma)

    subtotal_incluyendo_iva = sum(detalle.subtotal_prodProf for detalle in detalles_factura)
    porcentaje_iva = proforma.porcentaje_iva / 100
    subtotal = subtotal_incluyendo_iva / (1 + porcentaje_iva)
    total_iva = subtotal_incluyendo_iva - subtotal

    context = {
        'factura': proforma,
        'detalles_factura': detalles_factura,
        'subtotal': subtotal,
        'total_iva': total_iva,
        'tipo_documento': proforma.cliente.tipo_documento.nombre,
        'numero_documento': proforma.cliente.documento_cliente,
    }

    html_string = render_to_string('transactions/detalle_proforma.html', context)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        'page-size': 'A4',  # Establecer el tamaño de la página
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'load-error-handling': 'ignore',
        'no-stop-slow-scripts': '',
        'debug-javascript': '',
        'enable-local-file-access': '',
        'zoom': '1.25',  # Ajustar zoom si es necesario
    }
    pdf = pdfkit.from_string(html_string, False, configuration=config, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="proforma_{proforma.codigo}.pdf"'

    return response
