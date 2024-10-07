# finanzas/utils.py

from django.db.models import Sum
from datetime import datetime
from .models import Movimiento, MedioPago

def filtrar_movimientos_por_fecha(request):
    """Filtra los movimientos según el rango de fechas proporcionado."""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    # Inicializar las variables de fecha
    start_date = None
    end_date = None

    # Intentar convertir las cadenas de fecha a objetos datetime
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        # Manejar errores de formato de fecha
        start_date = end_date = None

    # Filtrar los movimientos según el rango de fechas si se proporcionan
    movimientos = Movimiento.objects.all()
    if start_date:
        movimientos = movimientos.filter(fecha__gte=start_date)
    if end_date:
        movimientos = movimientos.filter(fecha__lte=end_date)
    
    return movimientos, start_date_str, end_date_str

def calcular_totales(movimientos):
    """Calcula los totales de ingresos y salidas en pesos y dólares."""
    total_ingresos_pesos = movimientos.filter(tipo='INGRESO', moneda='PESOS').aggregate(total=Sum('monto'))['total'] or 0
    total_salidas_pesos = movimientos.filter(tipo='SALIDA', moneda='PESOS').aggregate(total=Sum('monto'))['total'] or 0
    total_ingresos_dolares = movimientos.filter(tipo='INGRESO', moneda='USD').aggregate(total=Sum('monto'))['total'] or 0
    total_salidas_dolares = movimientos.filter(tipo='SALIDA', moneda='USD').aggregate(total=Sum('monto'))['total'] or 0

    return {
        'total_ingresos_pesos': int(total_ingresos_pesos),
        'total_salidas_pesos': int(total_salidas_pesos),
        'total_ingresos_dolares': int(total_ingresos_dolares),
        'total_salidas_dolares': int(total_salidas_dolares),
    }

# finanzas/utils.py

def calcular_totales_por_medio_pago(movimientos):
    """
    Calcula los totales de ingresos y salidas por cada medio de pago.
    Retorna una lista de diccionarios con el nombre del medio de pago y los totales.
    """
    medios_pagos = MedioPago.objects.all()
    totales_medio_pago = []

    for medio in medios_pagos:
        ingresos = movimientos.filter(medio_pago=medio, tipo='INGRESO').aggregate(total=Sum('monto'))['total'] or 0
        salidas = movimientos.filter(medio_pago=medio, tipo='SALIDA').aggregate(total=Sum('monto'))['total'] or 0
        neto = int(ingresos) - int(salidas)
        
        totales_medio_pago.append({
            'id': medio.id,  # Añadido el ID
            'medio_pago': medio.nombre,
            'ingresos': int(ingresos),
            'salidas': int(salidas),
            'neto': neto,
        })
    
    return totales_medio_pago
