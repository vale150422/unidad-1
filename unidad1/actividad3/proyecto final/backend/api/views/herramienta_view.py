from rest_framework import viewsets
from api.models.herramienta import Herramienta
from project.serializers.herramienta_serializer import HerramientaSerializer
#ya agarraron los import, era que faltaba __init__.py en la ruta a importar, entonces django no reconocia la carpeta como un modulo

class HerramientaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Herramienta.
    """
    queryset = Herramienta.objects.all().order_by('codigo')
    serializer_class = HerramientaSerializer
    
    