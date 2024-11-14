from django import forms
from .models import Cotizacion, Detalles_Cotizacion, Proforma, Detalles_Proforma
from accounts.models import Cliente, Trabajador
from inventory.models import Producto, Medio_Pago, Forma_Pago
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.utils import timezone
from datetime import timedelta


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'trabajador', 'fecha_emision', 'fecha_vencimiento', 'descuento', 'total_iva', 'estado']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.Select(choices=[('Activo', 'Activo'), ('Cerrado', 'Cerrado'), ('Anulado', 'Anulado')]),
        }

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento', 0)
        if descuento and descuento < 0:
            raise ValidationError("El descuento no puede ser negativo.")
        return descuento

    def clean_total_iva(self):
        total_iva = self.cleaned_data.get('total_iva')
        if total_iva < 0:
            raise ValidationError("El total IVA no puede ser negativo.")
        return total_iva
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_emision'].initial = timezone.now().date()
        self.fields['fecha_vencimiento'].initial = (timezone.now() + timedelta(days=5)).date()
        self.fields['cliente'].widget.attrs.update({'class': 'form-select'})
        self.fields['trabajador'].widget.attrs.update({'class': 'form-select'})
        self.fields['fecha_emision'].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields['fecha_vencimiento'].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields['descuento'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_iva'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

class DetallesCotizacionForm(forms.ModelForm):
    iva_producto = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0, label='IVA (%)')

    class Meta:
        model = Detalles_Cotizacion
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal_prodC', 'iva_producto']
        widgets = {
            'producto': forms.Select(),
            'cantidad': forms.NumberInput(attrs={'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01'}),
            'subtotal_prodC': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'iva_producto': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad

    def clean_precio_unitario(self):
        precio_unitario = self.cleaned_data.get('precio_unitario')
        if precio_unitario <= 0:
            raise ValidationError("El precio unitario debe ser mayor a 0.")
        return precio_unitario

    def clean_subtotal_prodC(self):
        cantidad = self.cleaned_data.get('cantidad')
        precio_unitario = self.cleaned_data.get('precio_unitario')
        # Calcular el subtotal por producto
        return cantidad * precio_unitario

    def clean_iva_producto(self):
        iva_producto = self.cleaned_data.get('iva_producto')
        if iva_producto < 0:
            raise ValidationError("El IVA no puede ser negativo.")
        # Calcular el IVA basado en el precio unitario y cantidad
        subtotal_prodC = self.cleaned_data.get('subtotal_prodC')
        iva = (iva_producto / 100) * subtotal_prodC  # IVA en porcentaje
        return iva
    
# Crear un formset para los detalles de cotización
DetallesCotizacionFormSet = modelformset_factory(
    Detalles_Cotizacion,
    form=DetallesCotizacionForm,
    extra=1  # Esto agrega un formulario vacío adicional por defecto
)

class ProformaForm(forms.ModelForm):
    class Meta:
        model = Proforma
        fields = ['cliente', 'trabajador', 'medio_pago', 'forma_pago', 'fecha_emision', 'fecha_vencimiento', 'descuento', 'total_iva', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'trabajador': forms.Select(attrs={'class': 'form-control'}),
            'medio_pago': forms.Select(attrs={'class': 'form-control'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_iva': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

class DetallesProformaForm(forms.ModelForm):
    class Meta:
        model = Detalles_Proforma
        fields = ['proforma', 'producto', 'cantidad', 'subtotal_prodProf', 'precio_unitario', 'iva_producto']
        widgets = {
            'proforma': forms.HiddenInput(),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'subtotal_prodProf': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'iva_producto': forms.NumberInput(attrs={'class': 'form-control'})
        }
