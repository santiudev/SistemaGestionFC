from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name == 'users':
        # Crear grupos si no existen
        contadora_group, created = Group.objects.get_or_create(name='Contadora')
        visualizador_group, created = Group.objects.get_or_create(name='Visualizador')

        # Asignar permisos al grupo Contadora
        assign_permissions_to_contadora(contadora_group)

        # Asignar permisos al grupo Visualizador
        assign_permissions_to_visualizador(visualizador_group)

def assign_permissions_to_contadora(group):
    # Obtener todos los permisos de la app 'finanzas'
    finanzas_permissions = Permission.objects.filter(content_type__app_label='finanzas')
    group.permissions.set(finanzas_permissions)

def assign_permissions_to_visualizador(group):
    # Obtener permisos de visualización de la app 'finanzas'
    finanzas_content_types = ContentType.objects.filter(app_label='finanzas')
    view_permissions = Permission.objects.filter(content_type__in=finanzas_content_types, codename__startswith='view_')
    group.permissions.set(view_permissions)


@receiver(m2m_changed, sender=User.groups.through)
def update_user_role(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        groups = instance.groups.all()
        if groups:
            # Unir los nombres de los grupos en una cadena
            instance.rol = ', '.join([group.name for group in groups])
        else:
            instance.rol = ''
        instance.save()
