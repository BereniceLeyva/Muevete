from django.contrib import admin
from .models import Coche, Reserva, Auto, Promocion, Comentario

# Personalización del panel para Coche
from django.contrib import admin
from django.utils.html import format_html
from .models import Coche

class CocheAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/custom_admin.css',)  # tu CSS personalizado
        }
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'miniatura_catalogo', 'miniatura_top10', 'alcance', 'velocidad_maxima', 'costo', 'valoracion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('alcance',)
    date_hierarchy = 'created'
    fields = ('nombre','categoria', 'descripcion', 'alcance', 'velocidad_maxima', 'costo', 'valoracion',
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


# --- ADMIN Promocion ---
@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'coche', 'descuento', 'fecha_inicio', 'fecha_fin')
    search_fields = ('titulo', 'coche__nombre')
    list_filter = ('fecha_inicio', 'fecha_fin')

# --- ADMIN Comentario ---
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'coche', 'calificacion', 'fecha')
    search_fields = ('nombre', 'coche__nombre', 'texto')
    list_filter = ('calificacion', 'fecha')