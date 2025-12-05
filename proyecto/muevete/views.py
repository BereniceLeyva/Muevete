from django.shortcuts import render, get_object_or_404, redirect
from administrador.models import Coche, Reserva
from datetime import datetime
from administrador.models import Promocion
from administrador.models import Comentario

def home(request):
    return render(request, 'inicio/home.html')


def catalogo(request):
    coches = Coche.objects.all()
    return render(request, "inicio/catalogo.html", {"coches": coches})

def promociones(request):
    promos=Promocion.objects.all()
    return render(request, 'inicio/promociones.html', {"promos":promos})


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


def detalles_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    error = None  # Para mostrar mensajes en el template

    if request.method == "POST":
        if 'Comentario_submit' in request.POST:
            nombre=request.POST.get('nombre')
            texto = request.POST.get('texto')
            calificacion = int(request.POST.get('calificacion', 0))
            if nombre and texto:
                Comentario.objects.create(
                    coche=coche,
                    nombre=nombre,
                    texto=texto,
                    calificacion=calificacion
                )
            else:
                error = "Todos los campos del comentario son obligatorios."
        else:

            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            promo_code = request.POST.get("promo_code")

        # Convertimos las fechas a objetos datetime.date
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date_obj > end_date_obj:
                error = "La fecha de inicio no puede ser mayor a la de finalización."
            else:
                # Revisa si ya hay reservas que se solapen
                reservas_existentes = Reserva.objects.filter(
                    coche=coche,
                    start_date__lte=end_date_obj,
                    end_date__gte=start_date_obj
                )

                if reservas_existentes.exists():
                    error = "Este coche ya está reservado en las fechas seleccionadas."
                else:
                    # Crear la reserva si no hay conflicto
                    Reserva.objects.create(
                        coche=coche,
                        start_date=start_date_obj,
                        end_date=end_date_obj,
                        promo_code=promo_code
                    )
                    return redirect('reserva_exitosa')

        except ValueError:
            error = "Formato de fecha inválido."

    return render(request, "inicio/detallesCarro.html", {
        "coche": coche,
        "error": error
    })

def reserva_exitosa(request):
    return render(request, "inicio/reservaExitosa.html")


def alta_autos(request):
    return render(request, 'inicio/alta_autos.html')


def alta_registros(request):
    return render(request, 'inicio/registro.html')




