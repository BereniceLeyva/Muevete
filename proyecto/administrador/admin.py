from django.contrib import admin
from .models import Coche, Reserva

# Personalización del panel para Coche
class CocheAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nombre', 'alcance', 'velocidad_maxima', 'costo')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('alcance',)
    date_hierarchy = 'created'

# Personalización del panel para Reserva
class ReservaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('fecha_inicio', 'fecha_finalizacion', 'codigo_promocion')
    search_fields = ('codigo_promocion',)
    date_hierarchy = 'fecha_inicio'

# Registrar los modelos en el panel de administración
admin.site.register(Coche, CocheAdmin)
admin.site.register(Reserva, ReservaAdmin)
