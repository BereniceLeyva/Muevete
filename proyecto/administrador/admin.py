from django.contrib import admin
from .models import Coche, Reserva, Auto

# Personalización del panel para Coche
from django.contrib import admin
from django.utils.html import format_html
from .models import Coche

class CocheAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'miniatura_catalogo', 'miniatura_top10', 'alcance', 'velocidad_maxima', 'costo', 'valoracion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('alcance',)
    date_hierarchy = 'created'
    fields = ('nombre', 'descripcion', 'alcance', 'velocidad_maxima', 'costo', 'valoracion',
              'imagen_catalogo', 'imagen_top10', 'imagen_detalle', 'created', 'updated')

    # Miniatura para la imagen del catálogo
    def miniatura_catalogo(self, obj):
        if obj.imagen_catalogo:
            return format_html('<img src="{}" style="width: 60px; height:auto;">', obj.imagen_catalogo.url)
        return "-"
    miniatura_catalogo.short_description = "Imagen Catálogo"

    # Miniatura para la imagen del Top10
    def miniatura_top10(self, obj):
        if obj.imagen_top10:
            return format_html('<img src="{}" style="width: 60px; height:auto;">', obj.imagen_top10.url)
        return "-"
    miniatura_top10.short_description = "Imagen Top10"

admin.site.register(Coche, CocheAdmin)

# Personalización del panel para Reserva
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('coche', 'start_date', 'end_date', 'promo_code', 'created')
    list_filter = ('start_date', 'end_date')
    search_fields = ('coche__nombre', 'promo_code')
    date_hierarchy = 'start_date'


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'alcance', 'velocidad')
    search_fields = ('nombre',)