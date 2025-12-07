from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.herramienta import Herramienta
from api.models.prestamo import Prestamo
from api.serializers.herramienta_serializer import HerramientaSerializer
from api.serializers.prestamo_serializer import PrestamoSerializer



class BusquedaView(APIView):
    """
    Vista para búsqueda general de herramientas y préstamos.
    """

    def get(self, request):
        termino = request.GET.get("q", "").lower()

        herramientas = Herramienta.objects.filter(
            Q(codigo__icontains=termino) |
            Q(nombre__icontains=termino) |
            Q(categoria__icontains=termino)
        )

        prestamos = Prestamo.objects.filter(
            Q(numero__icontains=termino) |
            Q(responsable__icontains=termino) |
            Q(herramienta_codigo__icontains=termino)
        )

        herramientas_serializadas = HerramientaSerializer(
            herramientas,
            many=True
        ).data

        prestamos_serializados = PrestamoSerializer(
            prestamos,
            many=True
        ).data

        return Response({
            "herramientas": herramientas_serializadas,
            "prestamos": prestamos_serializados
        })
