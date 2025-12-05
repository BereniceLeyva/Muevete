from django.db import models

class Coche(models.Model):
    nombre = models.CharField(max_length=100)
    imagen_catalogo = models.ImageField(upload_to='coches/catalogo/')  # imagen para catálogo
    imagen_top10 = models.ImageField(upload_to='coches/top10/')        # imagen para Top10
    imagen_detalle = models.ImageField(upload_to='coches/detalles/', null=True, blank=True)  # imagen del detalle
    descripcion = models.TextField()
    alcance = models.CharField(max_length=50)
    velocidad_maxima = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    valoracion = models.IntegerField(default=0)
    CATEGORIAS = [
        ('DEPORTIVO', 'Deportivo'),
        ('ELECTRICO', 'Eléctrico'),
        ('LUJO', 'Lujo'),
    ]
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='DEPORTIVO')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def estrellas(self):
        return "⭐" * self.valoracion

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    promo_code = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.coche.nombre} del {self.start_date} al {self.end_date}"

class Promocion(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    descuento = models.CharField(max_length=20, blank=True, null=True) 
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.coche.nombre}"
    
class Comentario(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.CharField(max_length=100)
    texto = models.TextField()
    calificacion = models.PositiveIntegerField(default=0)  # estrellasrate
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.coche.nombre}"