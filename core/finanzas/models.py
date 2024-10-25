from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.conf import settings


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    requiere_patente = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class MedioPago(models.Model):
    MONEDA_CHOICES = [
        ('USD', 'Dólares'),
        ('PESOS', 'Pesos'),
    ]
    nombre = models.CharField(max_length=100)
    moneda = models.CharField(max_length=10, choices=MONEDA_CHOICES)
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
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    precio_dolar = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    precio_peso = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.tipo} - {self.categoria.nombre} - {self.monto} {self.moneda}"

    def clean(self):
        super().clean()
        if self.categoria.requiere_patente and not self.patente:
            raise ValidationError({'patente': 'Este campo es obligatorio para la categoría seleccionada.'})

    def save(self, *args, **kwargs):
        # Obtener la última cotización del dólar disponible
        from .models import CotizacionDolar  # Importación interna para evitar problemas de dependencia circular
        try:
            ultima_cotizacion = CotizacionDolar.objects.latest('fecha')
            cotizacion = ultima_cotizacion.valor_cotizacion
        except CotizacionDolar.DoesNotExist:
            raise ValidationError('No hay una cotización del dólar disponible.')

        # Calcular el precio en dólares y en pesos según la moneda seleccionada
        if self.moneda == 'USD':
            self.precio_dolar = self.monto
            self.precio_peso = self.monto * cotizacion
        elif self.moneda == 'PESOS':
            self.precio_peso = self.monto
            self.precio_dolar = self.monto / cotizacion

        super().save(*args, **kwargs)



class CotizacionDolar(models.Model):
    fecha = models.DateTimeField(unique=True, auto_now_add=True)
    valor_cotizacion = models.PositiveIntegerField()

    def __str__(self):
        return f'Cotización del {self.fecha}: {self.valor_cotizacion}'
    


class DocumentoAdjunto(models.Model):
    movimiento = models.ForeignKey(Movimiento, related_name='documentos_adjuntos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='finanzas/documentos_adjuntos/')

    def __str__(self):
        return f"Documento para Movimiento {self.movimiento.id}"