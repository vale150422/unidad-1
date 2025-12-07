from django.db import models
from django.db import transaction

class Prestamo(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    herramienta_codigo = models.CharField(max_length=50)
    responsable = models.CharField(max_length=200)
    fecha_salida = models.DateTimeField()
    fecha_esperada = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prestamo {self.numero} -> {self.herramienta_codigo}"

    @transaction.atomic
    def generar_numero_prestamo(self):
        ultimo = Prestamo.objects.order_by('id').last()
        if not ultimo:
            return "PR-001"

        numero = int(ultimo.numero.split("-")[1])
        return f"PR-{numero + 1:03d}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.generar_numero_prestamo()
        super().save(*args, **kwargs)
