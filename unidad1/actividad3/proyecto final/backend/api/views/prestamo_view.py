from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models.prestamo import Prestamo
from api.models.herramienta import Herramienta
from project.serializers.prestamo_serializer import PrestamoSerializer
#ya agarraron los import, era que faltaba __init__.py en la ruta a importar, entonces django no reconocia la carpeta como un modulo

from django.db import transaction

class PrestamoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Prestamo.
    Create: valida existencia y disponibilidad de la herramienta (por codigo),
            actualiza estado de herramienta a 'prestada'.
    Update: si se registra fecha_devolucion (antes nula) marca herramienta como 'disponible'.
    """
    queryset = Prestamo.objects.all().order_by('numero')
    serializer_class = PrestamoSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        codigo = data.get('herramienta_codigo')
        if not codigo:
            return Response({"error": "herramienta_codigo es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar herramienta
        try:
            herramienta = Herramienta.objects.select_for_update().get(codigo=codigo)
        except Herramienta.DoesNotExist:
            return Response({"error": "Herramienta no encontrada"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar disponibilidad
        if herramienta.estado.lower() != 'disponible':
            return Response({"error": "Herramienta no disponible"}, status=status.HTTP_400_BAD_REQUEST)

        # Serializar y guardar préstamo
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Actualizar estado de la herramienta a 'prestada'
        herramienta.estado = 'prestada'
        herramienta.save(update_fields=['estado', 'updated_at'])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        prev_fecha_devolucion = instance.fecha_devolucion

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_fecha_devolucion = serializer.instance.fecha_devolucion

        # Si se acaba de registrar fecha_devolucion (antes era None), liberar herramienta
        if new_fecha_devolucion and not prev_fecha_devolucion:
            try:
                herramienta = Herramienta.objects.select_for_update().get(codigo=serializer.instance.herramienta_codigo)
                herramienta.estado = 'disponible'
                herramienta.save(update_fields=['estado', 'updated_at'])
            except Herramienta.DoesNotExist:
                # No hacemos nada si no existe la herramienta referenciada
                pass

        return Response(serializer.data)




