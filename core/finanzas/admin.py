from django.contrib import admin
from .models import Categoria, MedioPago, Movimiento
# Register your models here.

admin.site.register(Categoria)
admin.site.register(MedioPago)
admin.site.register(Movimiento)
