from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from .forms import CategoriaForm, MedioPagoForm, FormaPagoForm, ProductoForm
from .models import Categoria, Medio_Pago, Forma_Pago, Producto, Historico_Precios

#Vista para crear Categorias
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Categoria
            categoria = form.save()
            # Redirigir a la vista de edición pasando el id de la nueva categoria
            return redirect('crear_categoria')
        else:
            print(form.errors)  # Imprimir los errores si el formulario no es válido
    else:
        form = CategoriaForm()

    categorias = Categoria.objects.all()  # Obtener todas las categorias
    estadoFuncion = 'crear'

    context = {
        'form': form,
        'categorias': categorias,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'inventory/categoria_form.html', context)


#Vista para editar Categorias
def editar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id=id_categoria)  # Obtener la categoria por id
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('crear_categoria')  # Redirigir a la lista de categorias
    else:
        form = CategoriaForm(instance=categoria)

    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'inventory/categoria_form.html', context)

#Vista para eliminar Categorias
def eliminar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id=id_categoria)  # Obtener la categoria por id
    if request.method == 'POST':
        categoria.delete()  # Eliminar la categoria
        return redirect('crear_categoria')  # Redirigir a la lista de categorias
    
    context = {
        'categoria': categoria,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'inventory/categoria_confirm_delete.html', context)

#Vista para crear Medio de Pago
def crear_medio_pago(request):
    if request.method == 'POST':
        form = MedioPagoForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Medio de Pago
            medio_pago = form.save()
            # Redirigir a la vista de edición pasando el id del nuevo medio de pago
            return redirect('crear_medio_pago')
        else:
            print(form.errors)  # Imprimir los errores si el formulario no es válido
    else:
        form = MedioPagoForm()

    medios_pago = Medio_Pago.objects.all()  # Obtener todos los medios de pago
    estadoFuncion = 'crear'

    context = {
        'form': form,
        'medios_pago': medios_pago,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'inventory/medio_pago_form.html', context)

#Vista para editar Medio de Pago
def editar_medio_pago(request, id_medio_pago):
    medio_pago = get_object_or_404(Medio_Pago, id=id_medio_pago)  # Obtener el medio de pago por id
    if request.method == 'POST':
        form = MedioPagoForm(request.POST, instance=medio_pago)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('crear_medio_pago')  # Redirigir a la lista de medios de pago
    else:
        form = MedioPagoForm(instance=medio_pago)

    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'inventory/medio_pago_form.html', context)

#Vista para eliminar Medio de Pago
def eliminar_medio_pago(request, id_medio_pago):
    medio_pago = get_object_or_404(Medio_Pago, id=id_medio_pago)  # Obtener el medio de pago por id
    if request.method == 'POST':
        medio_pago.delete()  # Eliminar el medio de pago
        return redirect('crear_medio_pago')  # Redirigir a la lista de medios de pago
    
    context = {
        'medio_pago': medio_pago,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'inventory/medio_pago_confirm_delete.html', context)



#Vista para crear Forma de Pago
def crear_forma_pago(request):
    if request.method == 'POST':
        form = FormaPagoForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Forma de Pago
            forma_pago = form.save()
            # Redirigir a la vista de edición pasando el id de la nueva forma de pago
            return redirect('crear_forma_pago')
        else:
            print(form.errors)  # Imprimir los errores si el formulario no es válido
    else:
        form = FormaPagoForm()

    formas_pago = Forma_Pago.objects.all()  # Obtener todas las formas de pago
    estadoFuncion = 'crear'

    context = {
        'form': form,
        'formas_pago': formas_pago,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'inventory/forma_pago_form.html', context)

#Vista para editar Forma de Pago
def editar_forma_pago(request, id_forma_pago):
    forma_pago = get_object_or_404(Forma_Pago, id=id_forma_pago)  # Obtener la forma de pago por id
    if request.method == 'POST':
        form = FormaPagoForm(request.POST, instance=forma_pago)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('crear_forma_pago')  # Redirigir a la lista de formas de pago
    else:
        form = FormaPagoForm(instance=forma_pago)

    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'inventory/forma_pago_form.html', context)


#Vista para eliminar Forma de Pago
def eliminar_forma_pago(request, id_forma_pago):
    forma_pago = get_object_or_404(Forma_Pago, id=id_forma_pago)  # Obtener la forma de pago por id
    if request.method == 'POST':
        forma_pago.delete()  # Eliminar la forma de pago
        return redirect('crear_forma_pago')  # Redirigir a la lista de formas de pago
    
    context = {
        'forma_pago': forma_pago,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'inventory/forma_pago_confirm_delete.html', context)

#Vista para crear Productos
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Producto
            producto = form.save()
            # Redirigir a la vista de creación de productos (o a una lista de productos)
            return redirect('crear_producto')  # Cambia esta URL por la que prefieras
        else:
            print(form.errors)  # Imprimir los errores si el formulario no es válido
    else:
        form = ProductoForm()

    productos = Producto.objects.all()  # Obtener todos los productos
    estadoFuncion = 'crear'  # Estado para indicar que estamos en la vista de creación

    context = {
        'form': form,
        'productos': productos,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'inventory/producto_form.html', context)

#Vista para editar Productos
def editar_producto(request, id_producto):
    try:
        # Obtener la instancia del producto
        producto_instance = Producto.objects.get(id=id_producto)
        
        # Manejar el formulario cuando el método es POST (actualización)
        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto_instance)
            if form.is_valid():
                form.save()  # Guardar los cambios en el producto
                return redirect('crear_producto')  # Redirigir a la lista de productos después de la actualización
        else:
            form = ProductoForm(instance=producto_instance)  # Prellenar el formulario con la instancia del producto

        # Obtener información adicional para el contexto, si es necesario
        productos = Producto.objects.all()
        categorias = Categoria.objects.all()  # Asumí que el modelo Producto tiene una relación con Categoría
        context = {
            'form': form,  # Pasa el formulario al contexto
            'productos': productos,  # Lista de productos
            'categorias': categorias,  # Lista de categorías para el campo 'categoria'
            'estadoFuncion': 'editar',  # Para saber si es una acción de edición
        }

        return render(request, 'inventory/producto_form.html', context)

    except Producto.DoesNotExist:
        raise Http404("Producto no encontrado")

#Vista para eliminar Productos
def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)  # Obtener el producto por id
    if request.method == 'POST':
        producto.delete()  # Eliminar el producto
        return redirect('crear_producto')  # Redirigir a la lista de productos (o la vista que prefieras)
    
    context = {
        'producto': producto,
        'estadoFuncion': 'eliminar',  # Indicamos que estamos en la vista de eliminación
    }
    return render(request, 'inventory/producto_confirm_delete.html', context)

#Historial de Precios
def historial_precio(request):
    # Obtener todos los registros del historial de precios
    historial = Historico_Precios.objects.all().order_by('-fecha_cambio')
    return render(request, 'inventory/historial_precio.html', {'historial': historial})