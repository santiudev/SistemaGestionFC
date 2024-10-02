from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    requiere_patente = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class MedioPago(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('SALIDA', 'Salida'),
    ]

    MONEDA_CHOICES = [
        ('USD', 'Dólares'),
        ('PESOS', 'Pesos'),
    ]


    fecha = models.DateField(default=date.today)

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    detalles = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=10, choices=MONEDA_CHOICES)
    comentario = models.TextField(blank=True, null=True)
    patente = models.CharField(max_length=10, blank=True, null=True)
    medio_pago = models.ForeignKey(MedioPago, on_delete=models.CASCADE)
    numero_comprobante = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    documento_adjunto = models.FileField(upload_to='finanzas/movimientos/', blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.categoria.nombre} - {self.monto} {self.moneda}"

    def clean(self):
        super().clean()
        if self.categoria.requiere_patente and not self.patente:
            raise ValidationError({'patente': 'Este campo es obligatorio para la categoría seleccionada.'})
