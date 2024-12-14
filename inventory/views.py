from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from .forms import CategoriaForm, MedioPagoForm, FormaPagoForm, ProductoForm
from .models import Categoria, Medio_Pago, Forma_Pago, Producto, Historico_Precios
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

#Vista para crear Categorias
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            return redirect('crear_producto')
        else:
            print(form.errors)
    else:
        form = ProductoForm()

    productos = Producto.objects.all().order_by('nombre')  # Ordenar los productos por nombre
    paginator = Paginator(productos, 10)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'estadoFuncion': 'crear',
    }
    return render(request, 'inventory/producto_form.html', context)

@login_required
def editar_producto(request, id_producto):
    try:
        producto_instance = Producto.objects.get(id=id_producto)
        
        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto_instance)
            if form.is_valid():
                form.save()
                return redirect('crear_producto')
        else:
            form = ProductoForm(instance=producto_instance)

        productos = Producto.objects.all().order_by('nombre')
        paginator = Paginator(productos, 10)  # Mostrar 10 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'form': form,
            'page_obj': page_obj,
            'estadoFuncion': 'editar',
        }
        return render(request, 'inventory/producto_form.html', context)
    
    except Producto.DoesNotExist:
        raise Http404("Producto no encontrado")


#Vista para eliminar Productos
@login_required
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
@login_required
def historial_precio(request):
    # Obtener todos los registros del historial de precios
    historial = Historico_Precios.objects.all().order_by('-fecha_cambio')
    return render(request, 'inventory/historial_precio.html', {'historial': historial})