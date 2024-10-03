from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from finanzas.models import Movimiento, Categoria, MedioPago

def assign_permissions_to_contadora():
    # Obtener el grupo Contadora
    contadora_group, _ = Group.objects.get_or_create(name='Contadora')

    # Obtener todos los permisos de la app finanzas
    finanzas_permissions = Permission.objects.filter(content_type__app_label='finanzas')

    # Asignar todos los permisos de finanzas al grupo Contadora
    contadora_group.permissions.set(finanzas_permissions)

def assign_permissions_to_visualizador():
    # Obtener el grupo Visualizador
    visualizador_group, _ = Group.objects.get_or_create(name='Visualizador')

    # Obtener permisos de visualización (view) de la app finanzas
    content_types = ContentType.objects.filter(app_label='finanzas')
    view_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')

    # Asignar permisos de visualización al grupo Visualizador
    visualizador_group.permissions.set(view_permissions)

def assign_all_permissions():
    assign_permissions_to_contadora()
    assign_permissions_to_visualizador()
