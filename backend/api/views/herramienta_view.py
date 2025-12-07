from rest_framework import viewsets
from api.models.herramienta import Herramienta
from api.serializers.herramienta_serializer import HerramientaSerializer

class HerramientaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Herramienta.
    Usa 'codigo' como lookup field en lugar de 'id'.
    """
    queryset = Herramienta.objects.all().order_by('codigo')
    serializer_class = HerramientaSerializer
    lookup_field = 'codigo'
    lookup_url_kwarg = 'codigo'
    