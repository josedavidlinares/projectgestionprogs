# transactions/views.py
from django.shortcuts import render, redirect
from .forms import CotizacionForm, DetallesCotizacionFormSet, DetallesCotizacionForm
from .models import Cotizacion, Detalles_Cotizacion, Producto
from django.http import JsonResponse, HttpResponse
import traceback

def crear_cotizacion(request):
    if request.method == 'POST':
        productos = []
        cotizacion_form = CotizacionForm(request.POST)

        # Verificar si el formulario de cotización es válido
        if cotizacion_form.is_valid():
            # Obtener los datos de la cotización
            cotizacion = cotizacion_form.save(commit=False)  # No guardar aún
            cotizacion.save()  # Guardamos la cotización para obtener su ID
            print(f"Cotización guardada con ID: {cotizacion.id}")

            # Obtener todos los campos que empiezan con 'productos_cantidad_'
            cantidad_campos = [key for key in request.POST if key.startswith('productos_cantidad_')]
            num_productos = len(cantidad_campos)  # El número total de productos

            # Recoger todos los productos
            for i in range(num_productos):
                # Comprobar si el campo 'productos_id_' está presente y tiene valor
                producto_id = request.POST.get(f'productos_id_{i}')

                # Verificar que el ID del producto no esté vacío o eliminado
                if not producto_id:
                    continue  # Si no hay producto, omitimos este detalle

                cantidad = request.POST.get(f'productos_cantidad_{i}')
                precio_unitario = request.POST.get(f'productos_precio_unitario_{i}')
                iva_producto = request.POST.get(f'productos_iva_producto_{i}')
                subtotal_prodC = request.POST.get(f'productos_subtotal_prodC_{i}')

                try:
                    # Obtener el producto desde la base de datos
                    producto = Producto.objects.get(id=producto_id)
                except ObjectDoesNotExist:
                    print(f"El producto con ID {producto_id} ya no existe o fue eliminado.")
                    continue  # Si el producto no existe, no lo agregamos

                # Crear el detalle de cotización
                detalle = Detalles_Cotizacion(
                    cotizacion=cotizacion,  # Asociar la cotización
                    producto=producto,      # Asociar el producto
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    iva_producto=iva_producto,
                    subtotal_prodC=subtotal_prodC
                )

                # Guardar el detalle de cotización
                detalle.save()

                # Imprimir en consola los detalles del producto
                print(f"Producto {i + 1}: {producto.nombre}, Cantidad: {cantidad}, Subtotal: {subtotal_prodC}")

            # Redirigir o mostrar una respuesta adecuada
            return redirect('crear_cotizacion')
        else:
            # Si el formulario de cotización no es válido, mostrar los errores
            print(f"Errores en el formulario de cotización: {cotizacion_form.errors}")

    else:
        cotizacion_form = CotizacionForm()

    return render(request, 'transactions/cotizacion.html', {
        'form': cotizacion_form,
        'detalle_form': DetallesCotizacionForm()
    })






def buscar_productos(request):
    try:
        query = request.GET.get('q', '')
        productos = Producto.objects.filter(nombre__icontains=query)
        productos_list = [{
            'id': producto.id,
            'codigo': producto.cod_producto,
            'nombre': producto.nombre,
            'precio': producto.precio_venta,
            'stock': producto.stock,
        } for producto in productos]
        print(productos_list)  # Verifica los datos en la consola
        return JsonResponse({'productos': productos_list})
    except Exception as e:
        print("Error en buscar_productos:", e)
        print(traceback.format_exc())  # Detalles del error
        return JsonResponse({'error': 'Ocurrió un error en el servidor.'}, status=500)