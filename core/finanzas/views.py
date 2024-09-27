from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movimiento, Categoria
from .forms import MovimientoForm, CategoriaForm

@login_required
def home_finanzas(request):
    return render(request, 'finanzas/home.html')

@login_required
def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'finanzas/lista_movimientos.html', {'movimientos': movimientos})

@login_required
def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST, request.FILES)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            return redirect('finanzas:lista_movimientos')
    else:
        form = MovimientoForm()
    return render(request, 'finanzas/crear_movimiento.html', {'form': form})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finanzas:home')
    else:
        form = CategoriaForm()
    return render(request, 'finanzas/crear_categoria.html', {'form': form})
