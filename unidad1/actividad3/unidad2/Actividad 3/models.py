from django.db import models
class Dibujo(models.Model):  
    Autor = models.CharField(max_length=10, unique=True) 
    tipo_Dibujo = models.CharField(max_length=100) 
    Valor = models.PositiveIntegerField()
    fecha_Realizacion = models.DateField()

    def _str_(self):
        return f"{self.Dibujo} - {self.Autor}"


