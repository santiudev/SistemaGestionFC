from django.shortcuts import render, redirect, get_object_or_404  # Añadir esta línea
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Agregar esta línea para importar messages
from .models import Movimiento, Categoria, MedioPago
from .forms import MovimientoForm, CategoriaForm, MedioPagoForm
from django.db.models import Sum  # Add this line to import Sum


def home_finanzas(request):
    # Obtener los últimos 5 movimientos ordenados por fecha descendente
    recent_movements = Movimiento.objects.order_by('-fecha')[:5]

    # Calcular totales
    total_ingresos = Movimiento.objects.filter(tipo='INGRESO').aggregate(total=Sum('monto'))['total'] or 0
    total_salidas = Movimiento.objects.filter(tipo='SALIDA').aggregate(total=Sum('monto'))['total'] or 0
    total_dolares = Movimiento.objects.filter(moneda='USD').aggregate(total=Sum('monto'))['total'] or 0
    total_pesos = Movimiento.objects.filter(moneda='PESOS').aggregate(total=Sum('monto'))['total'] or 0

    context = {
        'recent_movements': recent_movements,
        'total_ingresos': total_ingresos,
        'total_salidas': total_salidas,
        'total_dolares': total_dolares,
        'total_pesos': total_pesos,
    }

    return render(request, 'finanzas/home.html', context)


def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'finanzas/lista_movimientos.html', {'movimientos': movimientos})

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


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finanzas:home')
    else:
        form = CategoriaForm()
    categorias = Categoria.objects.all()
    return render(request, 'finanzas/crear_categoria.html', {'form': form, 'categorias': categorias})

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

def eliminar_medio_pago(request, medio_pago_id):
    medio_pago = get_object_or_404(MedioPago, id=medio_pago_id)  # Obtener el medio de pago
    medio_pago.delete()  # Eliminar el medio de pago
    messages.success(request, 'Medio de pago eliminado con éxito.')  # Mensaje de éxito
    return redirect('finanzas:crear_mediodepago.html')  # Redirigir a la vista deseada



def detalle_movimiento(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    return render(request, 'finanzas/detalle_movimiento.html', {'movimiento': movimiento})
