from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404  # Añadir esta línea
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages  # Agregar esta línea para importar messages
from .models import Movimiento, Categoria, MedioPago, CotizacionDolar
from .forms import MovimientoForm, CategoriaForm, MedioPagoForm, CotizacionDolarForm
from django.db.models import Sum  # Add this line to import Sum
from .utils import filtrar_movimientos_por_fecha, calcular_totales, calcular_totales_por_medio_pago
from django.utils import timezone


from datetime import datetime

@login_required
@permission_required('finanzas.view_movimiento', raise_exception=True)
def home_finanzas(request):
    # Filtrar los movimientos según el rango de fechas
    movimientos, start_date_str, end_date_str = filtrar_movimientos_por_fecha(request)
    
    # Formatear las fechas para mostrar en el formato "dd/mm/yyyy"
    if start_date_str:
        start_date_str = datetime.strptime(start_date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    if end_date_str:
        end_date_str = datetime.strptime(end_date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    # Obtener los últimos 5 movimientos ordenados por fecha descendente (sin filtrar)
    recent_movements = Movimiento.objects.all().order_by('-fecha')[:5]

    # Calcular totales sin decimales dentro del filtro
    totales = calcular_totales(movimientos)

    # Calcular totales por medio de pago dentro del filtro
    totales_medio_pago = calcular_totales_por_medio_pago(movimientos)

    # Obtener la última cotización del dólar
    try:
        ultima_cotizacion = CotizacionDolar.objects.latest('fecha')
        cotizacion_actual = ultima_cotizacion.valor_cotizacion
    except CotizacionDolar.DoesNotExist:
        cotizacion_actual = 0  # O un valor por defecto

    # Determinar los textos según si hay filtro de fecha aplicado o no
    if start_date_str and end_date_str:
        ingresos_pesos_label = f"Entradas de pesos\nDesde: {start_date_str}\nHasta: {end_date_str}"
        salidas_pesos_label = f"Salidas de pesos\nDesde: {start_date_str}\nHasta: {end_date_str}"
        ingresos_dolares_label = f"Entradas de dólares\nDesde: {start_date_str}\nHasta: {end_date_str}"
        salidas_dolares_label = f"Salidas de dólares\nDesde: {start_date_str}\nHasta: {end_date_str}"
    else:
        ingresos_pesos_label = "Entradas de pesos\nHistórico"
        salidas_pesos_label = "Salidas de pesos\nHistórico"
        ingresos_dolares_label = "Entradas de dólares\nHistórico"
        salidas_dolares_label = "Salidas de dólares\nHistórico"

    context = {
        'recent_movements': recent_movements,
        'total_ingresos_pesos': totales['total_ingresos_pesos'],
        'total_salidas_pesos': totales['total_salidas_pesos'],
        'total_ingresos_dolares': totales['total_ingresos_dolares'],
        'total_salidas_dolares': totales['total_salidas_dolares'],
        'start_date': start_date_str if start_date_str else '',
        'end_date': end_date_str if end_date_str else '',
        'totales_medio_pago': totales_medio_pago,
        'cotizacion_actual': cotizacion_actual,
        'ingresos_pesos_label': ingresos_pesos_label,
        'salidas_pesos_label': salidas_pesos_label,
        'ingresos_dolares_label': ingresos_dolares_label,
        'salidas_dolares_label': salidas_dolares_label,
    }

    return render(request, 'finanzas/home.html', context)




@login_required
@permission_required('finanzas.view_movimiento', raise_exception=True)
def lista_movimientos(request):
    categoria_id = request.GET.get('categoria')  # Obtener el ID de la categoría del query string
    fecha_inicio = request.GET.get('fecha_inicio')  # Obtener la fecha de inicio del query string
    fecha_fin = request.GET.get('fecha_fin')  # Obtener la fecha de fin del query string

    # Filtrar por fechas si están presentes
    if fecha_inicio and fecha_fin:
        movimientos = Movimiento.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by('-fecha')
    elif categoria_id:
        movimientos = Movimiento.objects.filter(categoria_id=categoria_id).order_by('-fecha')  # Filtrar por categoría
    else:
        movimientos = Movimiento.objects.all().order_by('-fecha')
        
    categorias = Categoria.objects.all()  # Obtener las categorías para el contexto
    medios_pago = MedioPago.objects.all()  # Obtener los medios de pago para el contexto
    return render(request, 'finanzas/lista_movimientos.html', {
        'movimientos': movimientos,
        'categorias': categorias,
        'medios_pago': medios_pago  # Asegúrate de pasar los medios de pago
    })

@login_required
@permission_required('finanzas.add_movimiento', raise_exception=True)
def crear_movimiento(request):
    # Verificar si se ha actualizado la cotización del dólar hoy
    today = timezone.now().date()
    cotizacion_actualizada_hoy = CotizacionDolar.objects.filter(fecha__date=today).exists()

    if request.method == 'POST':
        form = MovimientoForm(request.POST, request.FILES)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user  # Asocia el movimiento al usuario actual
            movimiento.save()
            return redirect('finanzas:lista_movimientos')  # Redirige a la lista de movimientos
    else:
        form = MovimientoForm()

    # Agregar medios de pago y categorías al contexto
    categorias = Categoria.objects.all()
    medios_pago = MedioPago.objects.all()

    context = {
        'form': form,
        'categorias': categorias,
        'medios_pago': medios_pago,
        'cotizacion_actualizada_hoy': cotizacion_actualizada_hoy
    }

    return render(request, 'finanzas/crear_movimiento.html', context)


@login_required
@permission_required('finanzas.add_movimiento', raise_exception=True)
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nueva_categoria')
        requiere_patente = 'requiere_patente' in request.POST
        if nombre:
            Categoria.objects.create(nombre=nombre, requiere_patente=requiere_patente)
        return redirect('finanzas:crear_categoria')
    categorias = Categoria.objects.all()
    return render(request, 'finanzas/crear_categoria.html', {'categorias': categorias})


@login_required
@permission_required('finanzas.add_movimiento', raise_exception=True)
def crear_mediopago(request):
       if request.method == 'POST':
           form = MedioPagoForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('finanzas:crear_mediodepago')
           else:
               # Agregar un mensaje de error
               messages.error(request, 'Error al crear el medio de pago. Verifica los datos.')
       else:
           form = MedioPagoForm()
       medios_pago = MedioPago.objects.all()
       return render(request, 'finanzas/crear_mediodepago.html', {'form': form, 'medios_pago': medios_pago})


@login_required
@permission_required('finanzas.delete_mediopago', raise_exception=True)
def eliminar_medio_pago(request, medio_pago_id):
    medio_pago = get_object_or_404(MedioPago, id=medio_pago_id)  # Obtener el medio de pago
    medio_pago.delete()  # Eliminar el medio de pago
    messages.success(request, 'Medio de pago eliminado con éxito.')  # Mensaje de éxito
    return redirect('finanzas:crear_mediodepago')  # Redirigir a la vista deseada


@login_required
@permission_required('finanzas.view_movimiento', raise_exception=True)
def detalle_movimiento(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    return render(request, 'finanzas/detalle_movimiento.html', {'movimiento': movimiento})


@login_required
@permission_required('finanzas.delete_categoria', raise_exception=True)  # Asegúrate de tener el permiso correcto
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)  # Obtener la categoría
    categoria.delete()  # Eliminar la categoría
    messages.success(request, 'Categoría eliminada con éxito.')  # Mensaje de éxito
    return redirect('finanzas:crear_categoria')  # Redirigir a la vista deseada


@login_required
@permission_required('finanzas.view_movimiento', raise_exception=True)
def detalle_medio_pago(request, medio_pago_id):
    # Obtener el medio de pago o devolver 404 si no existe
    medio_pago = get_object_or_404(MedioPago, id=medio_pago_id)
    
    # Obtener todos los movimientos asociados a este medio de pago, ordenados por fecha descendente
    movimientos = Movimiento.objects.filter(medio_pago=medio_pago).select_related('categoria').order_by('-fecha')
    
    # Calcular totales para mostrar en la plantilla
    total_ingresos = movimientos.filter(tipo='INGRESO').aggregate(total=Sum('monto'))['total'] or 0
    total_salidas = movimientos.filter(tipo='SALIDA').aggregate(total=Sum('monto'))['total'] or 0
    total_neto = int(total_ingresos) - int(total_salidas)
    
    context = {
        'medio_pago': medio_pago,
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_salidas': total_salidas,
        'total_neto': total_neto,
    }
    
    return render(request, 'finanzas/detalle_medio_pago.html', context)


@login_required
@permission_required('finanzas.add_movimiento', raise_exception=True)
def actualizar_cotizacion(request):
    if request.method == 'POST':
        # Crear una nueva instancia de CotizacionDolar con la fecha y hora actual
        nueva_cotizacion = CotizacionDolar(fecha=datetime.now(), valor_cotizacion=request.POST.get('valor_cotizacion'))

        # Crear el formulario con la nueva instancia
        form = CotizacionDolarForm(request.POST, instance=nueva_cotizacion)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cotización actualizada exitosamente.')
        else:
            messages.error(request, 'Formulario no válido. Por favor ingrese un valor válido.')

        return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la misma ruta
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la misma ruta si no es POST


@login_required
@permission_required('finanzas.delete_movimiento', raise_exception=True)
def eliminar_movimiento(request, movimiento_id):
    movimiento = get_object_or_404(Movimiento, id=movimiento_id)
    movimiento.delete()
    messages.success(request, 'Movimiento eliminado exitosamente.')
    return redirect('finanzas:lista_movimientos')


@login_required
@permission_required('finanzas.change_movimiento', raise_exception=True)
def editar_movimiento(request, movimiento_id):
    movimiento = get_object_or_404(Movimiento, id=movimiento_id)
    
    # Obtener la URL de referencia (HTTP_REFERER) para usar como 'next'
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', 'finanzas:lista_movimientos'))

    if request.method == 'POST':
        form = MovimientoForm(request.POST, request.FILES, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento actualizado exitosamente.')
            return redirect(next_url)  # Redirige a la URL previa
    else:
        form = MovimientoForm(instance=movimiento)

    # Agregar medios de pago y categorías al contexto
    categorias = Categoria.objects.all()
    medios_pago = MedioPago.objects.all()

    context = {
        'form': form,
        'categorias': categorias,
        'medios_pago': medios_pago,
        'movimiento': movimiento,
        'next_url': next_url,
    }

    return render(request, 'finanzas/editar_movimiento.html', context)

