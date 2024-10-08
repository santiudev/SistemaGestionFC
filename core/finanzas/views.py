from django.shortcuts import render, redirect, get_object_or_404  # Añadir esta línea
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages  # Agregar esta línea para importar messages
from .models import Movimiento, Categoria, MedioPago
from .forms import MovimientoForm, CategoriaForm, MedioPagoForm
from django.db.models import Sum  # Add this line to import Sum
from .utils import filtrar_movimientos_por_fecha, calcular_totales, calcular_totales_por_medio_pago

@login_required
@permission_required('finanzas.view_movimiento', raise_exception=True)
def home_finanzas(request):
    # Filtrar los movimientos según el rango de fechas
    movimientos, start_date_str, end_date_str = filtrar_movimientos_por_fecha(request)
    
    # Obtener los últimos 5 movimientos ordenados por fecha descendente (sin filtrar)
    recent_movements = Movimiento.objects.all().order_by('-fecha')[:5]

    # Calcular totales sin decimales dentro del filtro
    totales = calcular_totales(movimientos)

    # Calcular totales por medio de pago dentro del filtro
    totales_medio_pago = calcular_totales_por_medio_pago(movimientos)

    context = {
        'recent_movements': recent_movements,
        'total_ingresos_pesos': totales['total_ingresos_pesos'],
        'total_salidas_pesos': totales['total_salidas_pesos'],
        'total_ingresos_dolares': totales['total_ingresos_dolares'],
        'total_salidas_dolares': totales['total_salidas_dolares'],
        'start_date': start_date_str if start_date_str else '',
        'end_date': end_date_str if end_date_str else '',
        'totales_medio_pago': totales_medio_pago,
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

    return render(request, 'finanzas/crear_movimiento.html', {
        'form': form,
        'categorias': categorias,
        'medios_pago': medios_pago
    })

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