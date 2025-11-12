"""
URL configuration for Muevete project.

The `urlpatterns` list routes URLs to views.
For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from muevete import views
from administrador import views as views_admin  # 👈 para usar registros de coches
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # para login

urlpatterns = [
    # Administración de Django
    path('admin/', admin.site.urls),

    # Página principal
    path('', views.home, name='Home'),

    # Páginas de la app 'muevete'
    path('catalogo/', views.catalogo, name='Catalogo'),
    path('promociones/', views.promociones, name='Promociones'),
    path('contacto/', views.contacto, name='Contacto'),
    path('login/', auth_views.LoginView.as_view(template_name='inicio/login.html'), name='login'),
    path('top10/', views.top10, name='Top10'),

    # Páginas de la app 'administrador'
    path('coches/', views_admin.registros, name='Registros'),
]
if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
