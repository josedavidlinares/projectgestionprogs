from django import forms
from .models import T_Contribuyente, T_Documento, Pais, Estado_Region, Municipio, Cliente, Proveedor, Trabajador, Tipo_Usuario
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget

# Mixin para añadir la clase 'form-control' a todos los campos automáticamente
class BaseFormMixin:
    form_control_class = {'class': 'form-control'}

    def add_form_control(self):
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update(self.form_control_class)

# Formularios para modelos con BaseFormMixin aplicado

class T_ContribuyenteForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = T_Contribuyente
        fields = ['id', 'nombre', 'descripcion']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre


class T_DocumentoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = T_Documento
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()


class PaisForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()


class Estado_RegionForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Estado_Region
        fields = ['id', 'nombre', 'pais']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'nombre': forms.TextInput(),
            'pais': Select2Widget(attrs={'data-placeholder': 'Seleccione un país'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise ValidationError('El nombre de la región debe tener al menos 3 caracteres.')
        return nombre


class MunicipioForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ['id', 'nombre', 'estado']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'nombre': forms.TextInput(),
            'estado': Select2Widget(attrs={'data-placeholder': 'Seleccione una región'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()


class ClienteForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id', 'tipo_documento', 'documento_cliente', 'nombre', 'apellido', 'contribuyente', 'email', 'telefono', 'municipio', 'direccion', 'activo']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'tipo_documento': Select2Widget(attrs={'data-placeholder': 'Seleccione un tipo de documento'}),
            'documento_cliente': forms.TextInput(),
            'nombre': forms.TextInput(),
            'apellido': forms.TextInput(),
            'contribuyente': Select2Widget(attrs={'data-placeholder': 'Seleccione un contribuyente'}),
            'email': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'municipio': Select2Widget(attrs={'data-placeholder': 'Seleccione un municipio'}),
            'direccion': forms.TextInput(),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def clean_documento_cliente(self):
        documento_cliente = self.cleaned_data.get('documento_cliente')
        cliente_instance = self.instance  # Instancia del cliente que se está editando
        
        # Validación de unicidad solo si el valor del campo ha cambiado
        if documento_cliente != cliente_instance.documento_cliente:
            if Cliente.objects.filter(documento_cliente=documento_cliente).exists():
                raise ValidationError('Este número de documento ya está registrado.')

        return documento_cliente


class ProveedorForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['id', 'tipo_documento', 'documento_proveedor', 'nombre', 'contribuyente', 'email', 'telefono', 'municipio', 'direccion']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'tipo_documento': Select2Widget(attrs={'data-placeholder': 'Seleccione un tipo de documento'}),
            'documento_proveedor': forms.TextInput(),
            'nombre': forms.TextInput(),
            'contribuyente': Select2Widget(attrs={'data-placeholder': 'Seleccione un contribuyente'}),
            'email': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'municipio': Select2Widget(attrs={'data-placeholder': 'Seleccione un municipio'}),
            'direccion': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def clean_documento_proveedor(self):
        documento_proveedor = self.cleaned_data.get('documento_proveedor')
        proveedor_instance = self.instance  # Instancia del proveedor que se está editando
        
        # Validación de unicidad solo si el valor del campo ha cambiado
        if documento_proveedor != proveedor_instance.documento_proveedor:
            if Proveedor.objects.filter(documento_proveedor=documento_proveedor).exists():
                raise ValidationError('Este número de documento ya está registrado.')

        return documento_proveedor


class TrabajadorForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['id', 'tipo_documento', 'documento_trabajador', 'nombre', 'apellido', 'email', 'telefono', 'municipio', 'direccion', 'tipo_usuario', 'activo']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'tipo_documento': Select2Widget(attrs={'data-placeholder': 'Seleccione un tipo de documento'}),
            'documento_trabajador': forms.TextInput(),
            'nombre': forms.TextInput(),
            'apellido': forms.TextInput(),
            'email': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'municipio': Select2Widget(attrs={'data-placeholder': 'Seleccione un municipio'}),
            'direccion': forms.TextInput(),
            'tipo_usuario': Select2Widget(attrs={'data-placeholder': 'Seleccione un tipo de usuario'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    def clean_documento_trabajador(self):
        documento_trabajador = self.cleaned_data.get('documento_trabajador')
        trabajador_instance = self.instance  # Instancia del trabajador que se está editando
        
        # Validación de unicidad solo si el valor del campo ha cambiado
        if documento_trabajador != trabajador_instance.documento_trabajador:
            if Trabajador.objects.filter(documento_trabajador=documento_trabajador).exists():
                raise ValidationError('Este número de documento ya está registrado.')

        return documento_trabajador


class Tipo_UsuarioForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Tipo_Usuario
        fields = ['id', 'nombre', 'descripcion']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()


# Formulario de búsqueda personalizado para Cliente
class ClienteSearchForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
