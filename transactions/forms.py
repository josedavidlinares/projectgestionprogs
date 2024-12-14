from django import forms
from .models import Cotizacion, Detalles_Cotizacion, Proforma, Detalles_Proforma, PagoCredito
from accounts.models import Cliente, Trabajador
from inventory.models import Producto, Medio_Pago, Forma_Pago
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class CotizacionForm(forms.ModelForm):
    DESCUENTO_CHOICES = [
        (0, '0%'),
        (5, '5%'),
        (10, '10%'),
        # Agrega más opciones si es necesario
    ]

    PORCENTAJE_IVA_CHOICES = [
        (19, '19%'),
        (5, '5%'),
        (0, '0% Exento'),
    ]

    descuento = forms.ChoiceField(choices=DESCUENTO_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control bg-color'}))
    porcentaje_iva = forms.ChoiceField(choices=PORCENTAJE_IVA_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Cotizacion
        fields = ['cliente', 'trabajador', 'fecha_emision', 'fecha_vencimiento', 'porcentaje_iva', 'estado']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento', 0)
        try:
            descuento = Decimal(descuento)
        except ValueError:
            raise ValidationError("El descuento debe ser un número decimal válido.")
        
        if descuento < 0:
            raise ValidationError("El descuento no puede ser negativo.")
        return descuento

    def clean_porcentaje_iva(self):
        porcentaje_iva = self.cleaned_data.get('porcentaje_iva')

        # Asegurarse de que porcentaje_iva es un número
        if isinstance(porcentaje_iva, str):
            porcentaje_iva = porcentaje_iva.replace(',', '.')
            if porcentaje_iva.isdigit():
                porcentaje_iva = int(porcentaje_iva)
            else:
                try:
                    porcentaje_iva = float(porcentaje_iva)
                except ValueError:
                    raise ValidationError("Porcentaje IVA debe ser un número.")

        if porcentaje_iva < 0:
            raise ValidationError("El porcentaje de IVA no puede ser negativo.")
        return porcentaje_iva

    def clean_fecha_emision(self):
        fecha_emision = self.cleaned_data.get('fecha_emision')
        if fecha_emision > timezone.now().date():
            raise ValidationError("La fecha de emisión no puede ser en el futuro.")
        return fecha_emision

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        fecha_emision = self.cleaned_data.get('fecha_emision')
        if fecha_vencimiento and fecha_vencimiento <= fecha_emision:
            raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de emisión.")
        return fecha_vencimiento

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_emision'].initial = timezone.now().date()
        self.fields['fecha_vencimiento'].initial = (timezone.now() + timedelta(days=5)).date()
        self.fields['cliente'].widget.attrs.update({'class': 'form-select'})
        self.fields['trabajador'].widget.attrs.update({'class': 'form-select'})
        self.fields['descuento'].widget.attrs.update({'class': 'form-control'})
        self.fields['porcentaje_iva'].widget.attrs.update({'class': 'form-select'})
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})

class DetallesCotizacionForm(forms.ModelForm):

    class Meta:
        model = Detalles_Cotizacion
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'subtotal': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        if not isinstance(cantidad, int):
            raise ValidationError("La cantidad debe ser un número entero.")
        return cantidad

    def clean_precio_unitario(self):
        precio_unitario = self.cleaned_data.get('precio_unitario')
        if precio_unitario <= 0:
            raise ValidationError("El precio unitario debe ser mayor a 0.")
        if not re.match(r'^\d+(\.\d{1,2})?$', str(precio_unitario)):
            raise ValidationError("El precio unitario debe ser un número con hasta dos decimales.")
        return precio_unitario

    def clean_subtotal(self):
        cantidad = self.cleaned_data.get('cantidad')
        precio_unitario = self.cleaned_data.get('precio_unitario')
        subtotal = cantidad * precio_unitario
        return subtotal
    
# Crear un formset para los detalles de cotización
DetallesCotizacionFormSet = modelformset_factory(
    Detalles_Cotizacion,
    form=DetallesCotizacionForm,
    extra=1  # Esto agrega un formulario vacío adicional por defecto
)

#<------------------------------------------------------------------------------------------>

class ProformaForm(forms.ModelForm):
    DESCUENTO_CHOICES = [
        (5, '5%'),
        (10, '10%'),
    ]
    PORCENTAJE_IVA_CHOICES = [
        (19, '19%'),
        (5, '5%'),
        (0, '0% Exento'),
    ]
    descuento = forms.ChoiceField(choices=DESCUENTO_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control bg-color'}))
    porcentaje_iva = forms.ChoiceField(choices=PORCENTAJE_IVA_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Proforma
        fields = ['cliente', 'trabajador', 'medio_pago', 'forma_pago', 'fecha_emision', 'fecha_vencimiento', 'descuento', 'porcentaje_iva', 'estado', 'codigo']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'trabajador': forms.Select(attrs={'class': 'form-control'}),
            'medio_pago': forms.Select(attrs={'class': 'form-control'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descuento': forms.Select(attrs={'class': 'form-control'}),
            'porcentaje_iva': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento', 0)
        try:
            descuento = Decimal(descuento)
        except ValueError:
            raise ValidationError("El descuento debe ser un número decimal válido.")
        if descuento < 0:
            raise ValidationError("El descuento no puede ser negativo.")
        return descuento

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_emision'].initial = timezone.now().date()
        self.fields['fecha_vencimiento'].initial = (timezone.now() + timedelta(days=5)).date()
        self.fields['cliente'].widget.attrs.update({'class': 'form-select'})
        self.fields['trabajador'].widget.attrs.update({'class': 'form-select'})
        self.fields['medio_pago'].widget.attrs.update({'class': 'form-control'})
        self.fields['forma_pago'].widget.attrs.update({'class': 'form-control'})
        self.fields['descuento'].widget.attrs.update({'class': 'form-control'})
        self.fields['porcentaje_iva'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-select'})
        self.fields['codigo'].widget.attrs.update({'readonly': 'readonly'})

class DetallesProformaForm(forms.ModelForm):
    class Meta:
        model = Detalles_Proforma
        fields = ['proforma', 'producto', 'cantidad', 'subtotal_prodProf', 'precio_unitario']
        widgets = {
            'proforma': forms.HiddenInput(),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'subtotal_prodProf': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
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

    def clean_subtotal_prodProf(self):
        cantidad = self.cleaned_data.get('cantidad')
        precio_unitario = self.cleaned_data.get('precio_unitario')
        return cantidad * precio_unitario

class PagoCreditoForm(forms.ModelForm):
    class Meta:
        model = PagoCredito
        fields = ['proforma', 'monto_pagado']
        widgets = {
            'proforma': forms.Select(attrs={'class': 'form-control'}),
            'monto_pagado': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_monto_pagado(self):
        monto_pagado = self.cleaned_data.get('monto_pagado')
        if monto_pagado <= 0:
            raise ValidationError("El monto pagado debe ser mayor a 0.")
        return monto_pagado
