# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    celular = models.CharField(max_length=15)
    dni = models.CharField(max_length=15, unique=True)
    edad = models.PositiveIntegerField()
    rol = models.CharField(max_length=30, blank=True)
    foto = models.ImageField(upload_to='user_photos/', blank=True, null=True, default='user_photos/default.jpg')


    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'celular', 'dni', 'edad']
    def __str__(self):
        return f'{self.username} ({self.get_full_name()})'
