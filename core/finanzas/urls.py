from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.home_finanzas, name='home'),
    path('movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('movimientos/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
]
