from .forms import CotizacionDolarForm
from .models import CotizacionDolar

def cotizacion_context(request):
    # Obtener la última cotización si existe
    cotizacion = CotizacionDolar.objects.latest('fecha') if CotizacionDolar.objects.exists() else None
    valor_cotizacion = cotizacion.valor_cotizacion if cotizacion else ''
    form = CotizacionDolarForm(initial={'valor_cotizacion': valor_cotizacion})

    return {
        'cotizacion_form': form,
        'cotizacion_actual': valor_cotizacion
    }