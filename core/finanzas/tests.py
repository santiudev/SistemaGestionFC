# finanzas/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from users.models import CustomUser
from finanzas.models import Movimiento, Categoria, MedioPago

class MovimientoCreationTest(TestCase):
    def setUp(self):
        # Crear grupos
        self.contadora_group = Group.objects.create(name='Contadora')
        self.visualizador_group = Group.objects.create(name='Visualizador')

        # Asignar permisos
        view_permission = Permission.objects.get(codename='view_movimiento')
        add_permission = Permission.objects.get(codename='add_movimiento')
        self.contadora_group.permissions.add(view_permission, add_permission)
        self.visualizador_group.permissions.add(view_permission)

        # Crear usuarios
        self.contadora_user = CustomUser.objects.create_user(
            username='contadora',
            password='password123',
            email='contadora@example.com',
            nombre='Contadora',
            apellido='Ejemplo',
            celular='1234567890',
            dni='12345678A',
            edad=30
        )
        self.contadora_user.groups.add(self.contadora_group)

        self.visualizador_user = CustomUser.objects.create_user(
            username='visualizador',
            password='password123',
            email='visualizador@example.com',
            nombre='Visualizador',
            apellido='Ejemplo',
            celular='0987654321',
            dni='87654321B',
            edad=25
        )
        self.visualizador_user.groups.add(self.visualizador_group)

        # Crear categorías y medios de pago
        self.categoria = Categoria.objects.create(nombre='Venta', requiere_patente=False)
        self.medio_pago = MedioPago.objects.create(nombre='Efectivo')

        self.client = Client()

    def test_contadora_can_create_movimiento(self):
        self.client.login(username='contadora', password='password123')
        response = self.client.post(reverse('finanzas:crear_movimiento'), {
            'fecha': '2024-10-01',
            'tipo': 'INGRESO',
            'categoria': self.categoria.id,
            'detalles': 'Venta de producto',
            'monto': '1000.00',
            'moneda': 'USD',
            'comentario': 'Venta exitosa',
            'medio_pago': self.medio_pago.id,
            'numero_comprobante': 'ABC123',
        })
        self.assertEqual(response.status_code, 302)  # Redirige después de crear
        self.assertEqual(Movimiento.objects.count(), 1)
        movimiento = Movimiento.objects.first()
        self.assertEqual(movimiento.usuario, self.contadora_user)

    def test_visualizador_cannot_create_movimiento(self):
        self.client.login(username='visualizador', password='password123')
        response = self.client.post(reverse('finanzas:crear_movimiento'), {
            'fecha': '2024-10-01',
            'tipo': 'INGRESO',
            'categoria': self.categoria.id,
            'detalles': 'Venta de producto',
            'monto': '1000.00',
            'moneda': 'USD',
            'comentario': 'Venta exitosa',
            'medio_pago': self.medio_pago.id,
            'numero_comprobante': 'ABC123',
        })
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.assertEqual(Movimiento.objects.count(), 0)
