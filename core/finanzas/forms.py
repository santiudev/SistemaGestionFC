from django import forms
from .models import Movimiento, Categoria, MedioPago, CotizacionDolar

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['fecha', 'tipo', 'categoria', 'detalles', 'monto', 'moneda', 'comentario', 'patente', 'medio_pago', 'numero_comprobante', 'documento_adjunto']

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        self.fields['patente'].required = False
        self.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['fecha'].required = True
        self.fields['medio_pago'].queryset = MedioPago.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        patente = cleaned_data.get('patente')
        numero_comprobante = cleaned_data.get('numero_comprobante')

        # Asegurarse de que el campo "patente" sea obligatorio si la categoría lo requiere
        if categoria and categoria.requiere_patente and not patente:
            self.add_error('patente', 'Este campo es obligatorio para la categoría seleccionada.')

        # Si el número de comprobante es "None", dejarlo en blanco
        if numero_comprobante == 'None':
            cleaned_data['numero_comprobante'] = ''

        return cleaned_data


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
