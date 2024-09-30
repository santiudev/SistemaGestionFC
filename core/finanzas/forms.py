from django import forms
from .models import Movimiento, Categoria, MedioPago

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['fecha', 'tipo', 'categoria', 'detalles', 'monto', 'moneda', 'comentario', 'patente', 'medio_pago', 'numero_comprobante', 'documento_adjunto']

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        self.fields['patente'].required = False
        self.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['fecha'].required = True


    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        patente = cleaned_data.get('patente')

        if categoria and categoria.requiere_patente and not patente:
            self.add_error('patente', 'Este campo es obligatorio para la categoría seleccionada.')

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'requiere_patente']

class MedioPagoForm(forms.ModelForm):
    class Meta:
        model = MedioPago
        fields = ['nombre']