from django import forms
from .models import Categoria, Producto, Medio_Pago, Forma_Pago, Inventario, Historico_Precios, Ajuste_Stock
from django_select2.forms import Select2Widget

# Mixin para añadir la clase 'form-control' a todos los campos automáticamente
class BaseFormMixin:
    form_control_class = {'class': 'form-control'}

    def add_form_control(self):
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update(self.form_control_class)

# Formularios para modelos con BaseFormMixin aplicado
class CategoriaForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),  # Hacer el campo 'id' de solo lectura
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # Campo 'nombre' con clases para el estilo
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),  # Campo 'descripcion' con clases para el estilo
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()  # Agregar clases de control del formulario para el estilo

class MedioPagoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Medio_Pago
        fields = ['id', 'nombre', 'descripcion']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),  # Campo id solo lectura
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # Campo 'nombre' con clase 'form-control'
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),  # Campo 'descripcion' con clase 'form-control'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()  # Aplica clases de control para el formulario

class FormaPagoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Forma_Pago
        fields = ['id', 'nombre', 'descripcion']
        widgets = {
            'id': forms.NumberInput(attrs={'readonly': 'readonly'}),  # Campo id solo lectura
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # Campo 'nombre' con clase 'form-control'
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),  # Campo 'descripcion' con clase 'form-control'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()  # Aplica clases de control para el formulario

class ProductoForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['cod_producto', 'nombre', 'marca', 'categoria', 'stock', 'stock_min', 'stock_max', 'precio_venta', 'mercancia_muerta']
        widgets = {
            'cod_producto': forms.TextInput(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar
            'marca': forms.TextInput(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar
            'categoria': Select2Widget(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar y mantener Select2Widget
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar
            'stock_min': forms.NumberInput(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar
            'stock_max': forms.NumberInput(attrs={'class': 'form-control'}),  # Añadido 'form-control' para estilizar
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),  # Añadido 'form-control' para estilizar
            'mercancia_muerta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Añadido 'form-check-input' para estilizar el checkbox
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

    # Validación personalizada para asegurarse que el stock mínimo no sea mayor que el stock máximo
    def clean(self):
        cleaned_data = super().clean()
        stock_min = cleaned_data.get('stock_min')
        stock_max = cleaned_data.get('stock_max')

        if stock_min is not None and stock_max is not None and stock_min > stock_max:
            raise forms.ValidationError('El stock mínimo no puede ser mayor que el stock máximo.')
        
        return cleaned_data


class InventarioForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'fecha', 'proveedor', 'cantidad', 'n_lote', 'precio_cost']
        widgets = {
            'producto': Select2Widget(),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'proveedor': Select2Widget(),
            'cantidad': forms.NumberInput(),
            'n_lote': forms.TextInput(),
            'precio_cost': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

class HistoricoPreciosForm(forms.ModelForm):
    class Meta:
        model = Historico_Precios
        fields = ['producto', 'fecha_cambio', 'precio']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cambio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()

class Ajuste_StockForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Ajuste_Stock
        fields = ['producto', 'cantidad', 'motivo', 'fecha']
        widgets = {
            'producto': Select2Widget(),
            'cantidad': forms.NumberInput(),
            'motivo': forms.TextInput(),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form_control()
