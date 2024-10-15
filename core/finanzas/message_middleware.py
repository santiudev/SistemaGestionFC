from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class GlobalMessageMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Mensaje para la creación de medio de pago
        if request.method == 'POST' and view_func.__name__ == 'crear_mediodepago':
            messages.success(request, 'Medio de pago creado correctamente.')
        
        # Mensaje para la creación de movimiento
        elif request.method == 'POST' and view_func.__name__ == 'crear_movimiento':
            messages.success(request, 'Movimiento creado correctamente.')
        
        # Mensaje para la creación de categoría
        elif request.method == 'POST' and view_func.__name__ == 'crear_categoria':
            messages.success(request, 'Categoría creada correctamente.')
