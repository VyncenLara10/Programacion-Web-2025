from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Shoe(models.Model):
    SIZES = [(i, f"{i}") for i in range(34, 46)]  # shoe sizes 34–45
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    size = models.IntegerField(choices=SIZES)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='shoes/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Size {self.size})"