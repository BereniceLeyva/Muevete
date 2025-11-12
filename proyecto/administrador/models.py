from django.db import models

class Coche(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='coches/')  # usa MEDIA_URL
    descripcion = models.TextField()
    alcance = models.CharField(max_length=50)
    velocidad_maxima = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    valoracion = models.IntegerField(default=0)  # estrellas
    created = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated = models.DateTimeField(auto_now=True)
    def estrellas(self):
            return "⭐" * self.valoracion

    def __str__(self):
            return self.nombre
        
class Reserva(models.Model):
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    codigo_promocion = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva del {self.fecha_inicio} al {self.fecha_finalizacion}"
    
