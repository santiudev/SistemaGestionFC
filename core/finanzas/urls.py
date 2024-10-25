from django.urls import path
from . import views
from .views import eliminar_medio_pago, eliminar_categoria  # Asegúrate de importar la vista


app_name = 'finanzas'
urlpatterns = [
    path('', views.home_finanzas, name='home'),
    path('movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('movimientos/crear/', views.crear_movimiento, name='crear_movimiento'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('mediosdepago/crear/', views.crear_mediopago, name='crear_mediodepago'),
    path('mediopago/eliminar/<int:medio_pago_id>/', eliminar_medio_pago, name='eliminar_medio_pago'),
    path('categorias/eliminar/<int:id>/', eliminar_categoria, name='eliminar_categoria'), 
    path('movimientos/detalle/<int:id>/', views.detalle_movimiento, name='detalle_movimiento'),
    path('mediopagos/detalle/<int:medio_pago_id>/', views.detalle_medio_pago, name='detalle_medio_pago'),
    path('actualizar-cotizacion/', views.actualizar_cotizacion, name='actualizar_cotizacion'),
    path('eliminar-movimiento/<int:movimiento_id>/', views.eliminar_movimiento, name='eliminar_movimiento'),
    path('movimientos/editar/<int:movimiento_id>/', views.editar_movimiento, name='editar_movimiento'),  
    path('documento-adjunto/<int:documento_id>/eliminar/', views.eliminar_documento_adjunto, name='eliminar_documento_adjunto'),


]
