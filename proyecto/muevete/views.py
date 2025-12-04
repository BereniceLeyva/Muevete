from django.shortcuts import render
from administrador.models import Coche


def home(request):
    return render(request, 'inicio/home.html')


def catalogo(request):
    return render(request, 'inicio/catalogo.html')


def promociones(request):
    return render(request, 'inicio/promociones.html')


def coches(request):
    return render(request, 'inicio/coches.html')


def contacto(request):
    return render(request, 'inicio/contacto.html')

def top10(request):
    coches = Coche.objects.order_by('-valoracion')[:10]
    for coche in coches:
        coche.estrellas = "⭐" * coche.valoracion

    return render(request, 'inicio/top10.html', {'coches': coches})

def registro(request):
    return render(request, 'inicio/registro.html')

def detallesCarro(request, id=None):
    return render(request, 'inicio/detallesCarro.html')

def alta_autos(request):
    return render(request, 'inicio/alta_autos.html')
def alta_registros(request):
    return render(request, 'inicio/registro.html')