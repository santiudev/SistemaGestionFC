from django import forms
from .models import Movimiento, Categoria, MedioPago, CotizacionDolar

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['fecha', 'tipo', 'categoria', 'detalles', 'monto', 'moneda', 'comentario', 'patente', 'medio_pago', 'numero_comprobante']

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        self.fields['patente'].required = False
        self.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['fecha'].required = True


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'requiere_patente']

class MedioPagoForm(forms.ModelForm):
    class Meta:
        model = MedioPago
        fields = ['nombre', 'moneda']
        
        
class CotizacionDolarForm(forms.ModelForm):
    class Meta:
        model = CotizacionDolar
        fields = ['valor_cotizacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor_cotizacion'].label = "Cotización del Dólar"
