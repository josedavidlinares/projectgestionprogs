from django.shortcuts import render
from accounts.models import Cliente, Proveedor

def index(request):
    # Lógica para preparar datos para la página de inicio
    context = {}  # Contexto para pasar datos a la plantilla
    return render(request, 'index.html', context)

def dashboard(request, num_proveedor=5, num_cliente=5):
    # Ordenar los estados por su ID de forma descendente y limitar a los últimos 'num_estados'
    proveedores = Proveedor.objects.all().order_by('-id')[:num_proveedor]
    clientes = Cliente.objects.all().order_by('-id')[:num_cliente]

    context = {
        'proveedores': proveedores,
        'num_proveedor': num_proveedor,
        'clientes': clientes,
        'num_cliente': num_cliente,
    }
    
    return render(request, 'dashboard.html', context)