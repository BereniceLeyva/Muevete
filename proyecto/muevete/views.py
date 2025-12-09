from django.shortcuts import render, get_object_or_404, redirect
from administrador.models import Coche, Reserva, Auto
from datetime import datetime

from administrador.models import Promocion
from administrador.models import Comentario, MensajeContacto
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import logging


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


def top10(request):
    coches = Coche.objects.order_by('-valoracion')[:10]
    for coche in coches:
        coche.estrellas = "⭐" * coche.valoracion
    return render(request, 'inicio/top10.html', {'coches': coches})


def registro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("registro")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe.")
            return redirect("registro")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Ese correo ya está registrado.")
            return redirect("registro")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Usuario creado correctamente.")
        return redirect("login")  # A donde lo quieras mandar

    return render(request, "inicio/registro.html")


def detalles_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)
    error = None  # Para mostrar mensajes en el template

    if request.method == "POST":
        if 'comentario_submit' in request.POST:
            # Procesar comentarios
            nombre = request.POST.get('nombre')
            texto = request.POST.get('texto')
            calificacion = int(request.POST.get('calificacion', 0))
            if nombre and texto:
                Comentario.objects.create(
                    coche=coche,
                    nombre=nombre,
                    texto=texto,
                    calificacion=calificacion
                )
                return redirect('detalles_coche', coche_id=coche.id)
            else:
                error = "Todos los campos del comentario son obligatorios."

        else:
            # Formulario de reserva
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            promo_code = request.POST.get("promo_code")
            user_email = request.user.email if request.user.is_authenticated else request.POST.get("email")

            if not start_date or not end_date:
                error = "Debes seleccionar ambas fechas."
            elif not user_email:
                error = "Debes proporcionar un correo electrónico para la confirmación."
            else:
                try:
                    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

                    if start_date_obj > end_date_obj:
                        error = "La fecha de inicio no puede ser mayor a la de finalización."
                    else:
                        reservas_existentes = Reserva.objects.filter(
                            coche=coche,
                            start_date__lte=end_date_obj,
                            end_date__gte=start_date_obj
                        )

                        if reservas_existentes.exists():
                            error = "Este coche ya está reservado en las fechas seleccionadas."
                        else:
                            # Crear reserva
                            reserva = Reserva.objects.create(
                                coche=coche,
                                start_date=start_date_obj,
                                end_date=end_date_obj,
                                promo_code=promo_code
                            )

                            # Enviar correo de confirmación
                            try:
                                send_mail(
                                    subject='Confirmación de tu reserva',
                                    message=f'Hola {request.user.username if request.user.is_authenticated else "usuario"},\n\n'
                                            f'Tu reserva para el coche "{coche.nombre}" ha sido confirmada.\n'
                                            f'Fecha de inicio: {start_date}\n'
                                            f'Fecha de finalización: {end_date}\n'
                                            f'Código de promoción: {promo_code or "N/A"}\n\n'
                                            f'¡Gracias por confiar en nosotros!',
                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=[user_email],
                                    fail_silently=False,
                                )
                            except Exception as e:
                                # No interrumpe la reserva si falla el envío
                                print(f"Error al enviar correo: {e}")

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

logger = logging.getLogger(__name__)
def login_view(request):
    """
    Login que permite autenticación por email *o* username.
    En errores devuelve el template (no un redirect inmediato) para que
    se vea el mensaje inmediatamente y podamos debuggear.
    """
    if request.method == "POST":
        email_or_username = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        logger.debug("Intento de login para: %s", email_or_username)

        user = None

        # 1) si parece un email, buscamos primer usuario con ese email
        if "@" in email_or_username:
            u = User.objects.filter(email__iexact=email_or_username).first()
            if u:
                user = authenticate(request, username=u.username, password=password)
                logger.debug("Autenticando por email -> username=%s result=%s", u.username, bool(user))

        # 2) si no autenticó por email, intentar por username directo
        if user is None:
            user = authenticate(request, username=email_or_username, password=password)
            logger.debug("Autenticando por username=%s result=%s", email_or_username, bool(user))

        if user is not None:
            login(request, user)
            messages.success(request, "Has iniciado sesión correctamente.")
            logger.info("Login OK: %s", user.username)
            return redirect('inicio')  # cambia por la vista que quieras
        else:
            # No redirect inmediato: devolvemos template y mostramos mensaje.
            messages.error(request, "Usuario o contraseña incorrectos. Revisa tus datos.")
            logger.warning("Login fallido para: %s", email_or_username)
            # renderizamos la misma página con status 200 para que veas el mensaje
            return render(request, "inicio/login.html", status=200)

    # GET
    return render(request, "inicio/login.html")



def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('Home')



def alta_autos(request):
    if request.method == "POST":

        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        alcance = request.POST.get("alcance")
        velocidad = request.POST.get("velocidad")
        costo = request.POST.get("costo")
        imagen = request.FILES.get("car_image")

        Auto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            alcance=alcance,
            velocidad=velocidad,
            costo=costo,
            imagen=imagen
        )

        return redirect('Catalogo')  # o donde tú quieras

    return render(request, 'inicio/alta_autos.html')

def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        mensaje = request.POST.get("mensaje")

        # Guardar en BD
        MensajeContacto.objects.create(
            nombre=nombre,
            correo=correo,
            mensaje=mensaje
        )

        # Enviar correo
        send_mail(
            subject="Nuevo mensaje desde la página Muévete",
            message=f"Nombre: {nombre}\nCorreo: {correo}\n\nMensaje:\n{mensaje}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["mueveterecervas@gmail.com"],
        )

        return render(request, "inicio/contacto.html", {
            "exito": True
        })

    return render(request, "inicio/contacto.html")
