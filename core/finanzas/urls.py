from django.urls import path
from . import views
from .views import eliminar_medio_pago


app_name = 'finanzas'
urlpatterns = [
    path('', views.home_finanzas, name='home'),
    path('movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('movimientos/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('mediosdepago/crear/', views.crear_mediopago, name='crear_mediodepago'),
    path('mediopago/eliminar/<int:medio_pago_id>/', eliminar_medio_pago, name='eliminar_medio_pago'),
]
