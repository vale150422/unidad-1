
from django.db import models

class Herramienta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=100)  # disponible, prestada, dañada
    created_at = models.DateTimeField(auto_now_add=True)
    #se cree auto9maticamente la fecha de creacion
    updated_at = models.DateTimeField(auto_now=True)
    #se actualize automaticamente la fecha de actualizacion cuando se modifique
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    #
    def generar_codigo_herramienta(self):
        ultimo = Herramienta.objects.order_by("id").last()
        if not ultimo:
            return "HR-001"

        numero = int(ultimo.codigo.split("-")[1])
        return f"HR-{numero + 1:03d}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generar_codigo_herramienta()

        super().save(*args, **kwargs)
