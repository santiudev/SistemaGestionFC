from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Definir los campos que se mostrarán en el listado de usuarios
    list_display = ('username', 'email', 'nombre', 'apellido', 'celular', 'dni', 'edad', 'is_staff')
    search_fields = ('username', 'email', 'nombre', 'apellido', 'dni')
    ordering = ('username',)

    # Configurar los campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nombre', 'apellido', 'celular', 'dni', 'edad', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Configurar los campos en el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombre', 'apellido', 'celular', 'dni', 'edad', 'password1', 'password2'),
        }),
    )
