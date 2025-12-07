from django.contrib import admin
from .models.prestamo import Prestamo
from .models.herramienta import Herramienta


admin.site.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','categoria','ubicacion','estado','created_at')
    search_fields = ('codigo','nombre','categoria','ubicacion','estado')
    ordering = ('codigo',)

admin.site.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('numero','herramienta_codigo','responsable','fecha_salida','fecha_esperada','fecha_devolucion','created_at')
    search_fields = ('numero','herramienta_codigo','responsable')
    ordering = ('numero',)
