from django.shortcuts import render
from .models import Coche # Importa tu modelo de coches

# Vista para mostrar todos los coches registrados
def registros(request):
    coches = Coche.objects.all()  # Recupera todos los registros del modelo Coche
    return render(request, "inicio/coches.html", {'coches': coches})
