from django.shortcuts import render

def home(request):
    autos = {
        'Auto1': {'modelo': 'Modelo1', 'marca': 'Marca1', 'año': 2020, 'vendedor': 'Vendedor1', 'estado': 'vendido'},  # Agregado estado
        'Auto2': {'modelo': 'Modelo2', 'marca': 'Marca2', 'año': 2021, 'vendedor': 'Vendedor2', 'estado': 'disponible'},  # Agregado estado
        # ... más autos ...
    }

    if request.method == 'POST':
        for auto in autos.keys():
            estado = request.POST.get(auto)
            if estado:
                autos[auto]['estado'] = estado  # Actualiza el estado del auto

    return render(request, 'users/home.html', {'autos': autos})