from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from .models import T_Contribuyente, T_Documento, Pais, Estado_Region, Municipio, Cliente, Proveedor, Trabajador, Tipo_Usuario
from .forms import T_ContribuyenteForm, T_DocumentoForm, PaisForm, Estado_RegionForm, MunicipioForm, ClienteForm, ProveedorForm, TrabajadorForm, Tipo_UsuarioForm
from django.contrib.auth.decorators import login_required


# Vista para crear un T_Contribuyente
@login_required
def crear_t_contribuyente(request):
    if request.method == 'POST':
        form = T_ContribuyenteForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto T_Contribuyente
            t_contribuyente = form.save()
            # Redirigir a la vista de edición pasando el id (que en el modelo es 'id', no 'id_tcont')
            return redirect('crear_t_contribuyente')  # Usando 'id' en lugar de 'id_tcont'
        else:
            print(form.errors)
    else:
        form = T_ContribuyenteForm()

    tcontribuyentes = T_Contribuyente.objects.all()
    estadoFuncion = 'crear'
    
    context = {
        'form': form,
        'tcontribuyentes': tcontribuyentes,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'accounts/tcontribuyente_form.html', context)



# Vista para editar un T_Contribuyente
@login_required
def editar_t_contribuyente(request, id_tcont):
    t_contribuyente = get_object_or_404(T_Contribuyente, id=id_tcont)  # Asegúrate de que 'id' esté siendo usado aquí
    if request.method == 'POST':
        form = T_ContribuyenteForm(request.POST, instance=t_contribuyente)
        if form.is_valid():
            form.save()
            return redirect('crear_t_contribuyente')  # Redirige a la lista o página adecuada
    else:
        form = T_ContribuyenteForm(instance=t_contribuyente)
    
    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'accounts/tcontribuyente_form.html', context)


# Vista para eliminar un T_Contribuyente
@login_required
def eliminar_t_contribuyente(request, id_tcont):
    t_contribuyente = get_object_or_404(T_Contribuyente, id=id_tcont)  # Asegúrate de que 'id' esté siendo usado aquí
    if request.method == 'POST':
        t_contribuyente.delete()
        return redirect('crear_t_contribuyente')  # Redirige a la lista o página adecuada
    
    context = {
        't_contribuyente': t_contribuyente,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/tcontribuyente_confirm_delete.html', context)



# Vista para crear un T_Documento
@login_required
def crear_t_documento(request):
    if request.method == 'POST':
        form = T_DocumentoForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto T_Documento
            t_documento = form.save()
            # Redirigir a la vista de creación o a una lista de documentos
            return redirect('crear_t_documento')
        else:
            # Imprimir los errores del formulario en la consola (útil para depuración)
            print(form.errors)
    else:
        form = T_DocumentoForm()

    # Obtener todos los documentos existentes para mostrarlos en la página
    tdocumentos = T_Documento.objects.all()
    estadoFuncion = 'crear'
    
    context = {
        'form': form,
        'tdocumentos': tdocumentos,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'accounts/tdocumento_form.html', context)

# Vista para editar un T_Documento
@login_required
def editar_t_documento(request, id_doc):
    t_documento = get_object_or_404(T_Documento, id=id_doc)
    if request.method == 'POST':
        form = T_DocumentoForm(request.POST, instance=t_documento)
        if form.is_valid():
            form.save()
            return redirect('crear_t_documento')  # Redirige a la vista de creación o lista de documentos
    else:
        form = T_DocumentoForm(instance=t_documento)
    
    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'accounts/tdocumento_form.html', context)

# Vista para eliminar un T_Documento
@login_required
def eliminar_t_documento(request, id_doc):
    t_documento = get_object_or_404(T_Documento, id=id_doc)
    if request.method == 'POST':
        t_documento.delete()
        return redirect('crear_t_documento')  # Redirige a la lista o página adecuada
    
    context = {
        't_documento': t_documento,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/tdocumento_confirm_delete.html', context)


# Vista para crear un Pais
@login_required
def crear_pais(request):
    if request.method == 'POST':
        form = PaisForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto País
            pais = form.save()
            # Redirigir a la vista de creación o a una lista de países
            return redirect('crear_pais')
        else:
            # Imprimir los errores del formulario en la consola (útil para depuración)
            print(form.errors)
    else:
        form = PaisForm()

    # Obtener todos los países existentes para mostrarlos en la página
    paises = Pais.objects.all()
    estadoFuncion = 'crear'
    
    context = {
        'form': form,
        'paises': paises,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'accounts/pais_form.html', context)

# Vista para editar un Pais
@login_required
def editar_pais(request, id_pais):
    pais = get_object_or_404(Pais, id=id_pais)
    if request.method == 'POST':
        form = PaisForm(request.POST, instance=pais)
        if form.is_valid():
            form.save()
            return redirect('crear_pais')  # Redirige a la vista de creación o lista de países
    else:
        form = PaisForm(instance=pais)
    
    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'accounts/pais_form.html', context)

# Vista para eliminar un Pais
@login_required
def eliminar_pais(request, id_pais):
    pais = get_object_or_404(Pais, id=id_pais)
    if request.method == 'POST':
        pais.delete()
        return redirect('crear_pais')  # Redirige a la lista o página adecuada
    
    context = {
        'pais': pais,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/pais_confirm_delete.html', context)


# Vista para crear un Estado_Region
@login_required
def crear_estado_region(request):
    if request.method == 'POST':
        form = Estado_RegionForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Estado_Region
            estado_region = form.save()
            # Redirigir a la vista de creación o a la lista de estados/regiones
            return redirect('crear_estado_region')
        else:
            # Imprimir los errores del formulario en la consola (útil para depuración)
            print(form.errors)
    else:
        form = Estado_RegionForm()

    # Obtener todos los estados o regiones existentes para mostrarlos en la página
    estados_regiones = Estado_Region.objects.all()
    estadoFuncion = 'crear'
    
    context = {
        'form': form,
        'estados_regiones': estados_regiones,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'accounts/estado_region_form.html', context)

# Vista para editar un Estado_Region
@login_required
def editar_estado_region(request, id_estado):
    estado_region = get_object_or_404(Estado_Region, id=id_estado)
    if request.method == 'POST':
        form = Estado_RegionForm(request.POST, instance=estado_region)
        if form.is_valid():
            form.save()
            return redirect('crear_estado_region')  # Redirige a la vista de creación o lista de estados/regiones
    else:
        form = Estado_RegionForm(instance=estado_region)
    
    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'accounts/estado_region_form.html', context)

# Vista para eliminar un Estado_Region
@login_required
def eliminar_estado_region(request, id_estado):
    estado_region = get_object_or_404(Estado_Region, id=id_estado)
    if request.method == 'POST':
        estado_region.delete()
        return redirect('crear_estado_region')  # Redirige a la lista o página adecuada
    
    context = {
        'estado_region': estado_region,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/estado_region_confirm_delete.html', context)

@login_required
def obtener_paises(request):
    paises = Pais.objects.all().values('id', 'nombre')
    return JsonResponse(list(paises), safe=False)


# Vista para crear un Municipio
@login_required
def crear_municipio(request):
    if request.method == 'POST':
        form = MunicipioForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Municipio
            municipio = form.save()
            # Redirigir a la vista de creación o a la lista de municipios
            return redirect('crear_municipio')
        else:
            # Imprimir los errores del formulario en la consola (útil para depuración)
            print(form.errors)
    else:
        form = MunicipioForm()

    # Obtener todos los municipios existentes para mostrarlos en la página
    municipios = Municipio.objects.all()
    estadoFuncion = 'crear'
    
    context = {
        'form': form,
        'municipios': municipios,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'accounts/municipio_form.html', context)

# Vista para editar un Municipio
@login_required
def editar_municipio(request, id_municipio):
    municipio = get_object_or_404(Municipio, id=id_municipio)
    if request.method == 'POST':
        form = MunicipioForm(request.POST, instance=municipio)
        if form.is_valid():
            form.save()
            return redirect('crear_municipio')  # Redirige a la vista de creación o lista de municipios
    else:
        form = MunicipioForm(instance=municipio)
    
    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'accounts/municipio_form.html', context)

# Vista para eliminar un Municipio
@login_required
def eliminar_municipio(request, id_municipio):
    municipio = get_object_or_404(Municipio, id=id_municipio)
    if request.method == 'POST':
        municipio.delete()
        return redirect('crear_municipio')  # Redirige a la lista o página adecuada
    
    context = {
        'municipio': municipio,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/municipio_confirm_delete.html', context)

@login_required
def obtener_departamentos(request):
    # Obtener todos los departamentos de la base de datos
    departamentos = Estado_Region.objects.all()

    # Crear una lista de diccionarios con el id y nombre de cada departamento
    departamentos_data = [
        {'id': departamento.id, 'nombre': departamento.nombre}
        for departamento in departamentos
    ]

    # Devolver la lista como una respuesta JSON
    return JsonResponse(departamentos_data, safe=False)


# Vista para Crear un Cliente
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Cliente
            cliente = form.save()
            # Redirigir a la vista de creación o de detalles pasando el id del nuevo cliente
            return redirect('crear_cliente')
        else:
            print(form.errors)
    else:
        form = ClienteForm()

    # Obtener todos los clientes para mostrar en el listado
    clientes = Cliente.objects.all()

    context = {
        'form': form,
        'clientes': clientes,
        'estadoFuncion': 'crear',  # Esto puede ayudar a controlar qué tipo de acción se está haciendo
    }
    return render(request, 'accounts/cliente_form.html', context)


# Vista para Editar un Cliente
@login_required
def editar_cliente(request, id_cliente):
    try:
        cliente_instance = Cliente.objects.get(id=id_cliente)
        if request.method == 'POST':
            form = ClienteForm(request.POST, instance=cliente_instance)
            if form.is_valid():
                form.save()
                return redirect('crear_cliente')  # Redirigir a la lista de clientes
        else:
            form = ClienteForm(instance=cliente_instance)

        
        # Pasar los datos relacionados al contexto
        clientes = Cliente.objects.all()
        municipios = Municipio.objects.all()
        tdocumentos = T_Documento.objects.all()
        tcontribuyentes = T_Contribuyente.objects.all()

        context = {
            'form': form,  # Cambié Cliente_Form a form para que coincida con el template
            'clientes': clientes,
            'municipios': municipios,
            'tdocumentos': tdocumentos,
            'tcontribuyentes': tcontribuyentes,
            'estadoFuncion': 'editar',
        }

        return render(request, 'accounts/cliente_form.html', context)
    except Cliente.DoesNotExist:
        raise Http404("Cliente no encontrado")




# Vista para Eliminar un Cliente
@login_required
def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id=id_cliente)
    if request.method == 'POST':
        cliente.delete()
        return redirect('crear_cliente')  # Redirige a la lista de clientes

    context = {
        'cliente': cliente,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/cliente_form.html', context)

# Vista para Crear un Proveedor
@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Proveedor
            proveedor = form.save()
            # Redirigir a la vista de creación o de detalles pasando el id del nuevo proveedor
            return redirect('crear_proveedor')
        else:
            print(form.errors)
    else:
        form = ProveedorForm()

    # Obtener todos los proveedores para mostrar en el listado
    proveedores = Proveedor.objects.all()

    context = {
        'form': form,
        'proveedores': proveedores,
        'estadoFuncion': 'crear',  # Esto puede ayudar a controlar qué tipo de acción se está haciendo
    }
    return render(request, 'accounts/proveedor_form.html', context)

# Vista para Editar un Proveedor
@login_required
def editar_proveedor(request, id_proveedor):
    try:
        proveedor_instance = get_object_or_404(Proveedor, id=id_proveedor)  # Obtener el proveedor por id
        
        if request.method == 'POST':
            form = ProveedorForm(request.POST, instance=proveedor_instance)
            if form.is_valid():
                form.save()
                return redirect('crear_proveedor')  # Redirigir a la lista de proveedores o vista de detalles
        else:
            form = ProveedorForm(instance=proveedor_instance)

        # Pasar los datos relacionados al contexto
        proveedores = Proveedor.objects.all()
        municipios = Municipio.objects.all()
        tdocumentos = T_Documento.objects.all()
        tcontribuyentes = T_Contribuyente.objects.all()

        context = {
            'form': form,
            'proveedores': proveedores,
            'municipios': municipios,
            'tdocumentos': tdocumentos,
            'tcontribuyentes': tcontribuyentes,
            'estadoFuncion': 'editar',
        }

        return render(request, 'accounts/proveedor_form.html', context)
    except Proveedor.DoesNotExist:
        raise Http404("Proveedor no encontrado")
    
# Vista para Eliminar un Proveedor
@login_required
def eliminar_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, id=id_proveedor)  # Obtener el proveedor por id

    if request.method == 'POST':
        proveedor.delete()  # Eliminar el proveedor
        return redirect('crear_proveedor')  # Redirigir a la lista de proveedores

    context = {
        'proveedor': proveedor,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/proveedor_form.html', context)


#Vista para crear un Trabajador
@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Trabajador
            trabajador = form.save()
            # Redirigir a la vista de creación o de detalles pasando el id del nuevo trabajador
            return redirect('crear_trabajador')
        else:
            print(form.errors)
    else:
        form = TrabajadorForm()

    # Obtener todos los trabajadores para mostrar en el listado
    trabajadores = Trabajador.objects.all()

    context = {
        'form': form,
        'trabajadores': trabajadores,
        'estadoFuncion': 'crear',  # Esto puede ayudar a controlar qué tipo de acción se está haciendo
    }
    return render(request, 'accounts/trabajador_form.html', context)


#Vista para editar un Trabajador
@login_required
def editar_trabajador(request, id_trabajador):
    try:
        trabajador_instance = Trabajador.objects.get(id=id_trabajador)
        if request.method == 'POST':
            form = TrabajadorForm(request.POST, instance=trabajador_instance)
            if form.is_valid():
                form.save()
                return redirect('crear_trabajador')  # Redirigir a la lista de trabajadores
        else:
            form = TrabajadorForm(instance=trabajador_instance)

        # Obtener los datos relacionados para pasarlos al contexto
        trabajadores = Trabajador.objects.all()
        municipios = Municipio.objects.all()
        tdocumentos = T_Documento.objects.all()
        tcontribuyentes = T_Contribuyente.objects.all()

        context = {
            'form': form,  # El formulario de trabajador
            'trabajadores': trabajadores,
            'municipios': municipios,
            'tdocumentos': tdocumentos,
            'tcontribuyentes': tcontribuyentes,
            'estadoFuncion': 'editar',  # Indicador de que estamos editando
        }

        return render(request, 'accounts/trabajador_form.html', context)
    except Trabajador.DoesNotExist:
        raise Http404("Trabajador no encontrado")
    

#Vista para eliminar un Trabajador
@login_required
def eliminar_trabajador(request, id_trabajador):
    trabajador = get_object_or_404(Trabajador, id=id_trabajador)  # Obtener el trabajador por id

    if request.method == 'POST':
        trabajador.delete()  # Eliminar el trabajador
        return redirect('crear_trabajador')  # Redirigir a la lista de trabajadores

    context = {
        'trabajador': trabajador,
        'estadoFuncion': 'eliminar',  # Indicamos que estamos en la función de eliminar
    }
    return render(request, 'accounts/trabajador_form.html', context)

@login_required
def crear_tipo_usuario(request):
    if request.method == 'POST':
        form = Tipo_UsuarioForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo objeto Tipo_Usuario
            tipo_usuario = form.save()
            return redirect('crear_tipo_usuario')  # Redirigir a la vista de crear después de guardar
        else:
            print(form.errors)
    else:
        form = Tipo_UsuarioForm()

    tipo_usuarios = Tipo_Usuario.objects.all()
    estadoFuncion = 'crear'
    
    context = {
        'form': form,
        'tipo_usuarios': tipo_usuarios,
        'estadoFuncion': estadoFuncion,
    }
    return render(request, 'accounts/tipo_usuario_form.html', context)

@login_required
def editar_tipo_usuario(request, id):
    tipo_usuario = get_object_or_404(Tipo_Usuario, id=id)  # Usamos 'id' para obtener el objeto
    if request.method == 'POST':
        form = Tipo_UsuarioForm(request.POST, instance=tipo_usuario)
        if form.is_valid():
            form.save()
            return redirect('crear_tipo_usuario')  # Redirige después de guardar
    else:
        form = Tipo_UsuarioForm(instance=tipo_usuario)
    
    context = {
        'form': form,
        'estadoFuncion': 'editar',
    }
    return render(request, 'accounts/tipo_usuario_form.html', context)

@login_required
def eliminar_tipo_usuario(request, id):
    tipo_usuario = get_object_or_404(Tipo_Usuario, id=id)  # Usamos 'id' para obtener el objeto
    if request.method == 'POST':
        tipo_usuario.delete()
        return redirect('crear_tipo_usuario')  # Redirige después de eliminar
    
    context = {
        'tipo_usuario': tipo_usuario,
        'estadoFuncion': 'eliminar',
    }
    return render(request, 'accounts/tipo_usuario_confirm_delete.html', context)