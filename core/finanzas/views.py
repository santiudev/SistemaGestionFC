from django.shortcuts import render, redirect, get_object_or_404  # Añadir esta línea
from django.contrib.auth.decorators import login_required
from .models import Movimiento, Categoria, MedioPago
from .forms import MovimientoForm, CategoriaForm

def home_finanzas(request):
    return render(request, 'finanzas/home.html')

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
    return render(request, 'finanzas/crear_categoria.html', {'form': form})
