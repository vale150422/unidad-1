from rest_framework import serializers
from api.models.herramienta import Herramienta
from api.models.prestamo import Prestamo


class PrestamoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prestamo
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):
        codigo = data.get("herramienta_codigo")
        herramienta = Herramienta.objects.filter(codigo=codigo).first()

        if not herramienta:
            raise serializers.ValidationError("La herramienta no existe.")

        if herramienta.estado != "disponible":
            raise serializers.ValidationError("La herramienta no está disponible.")

        return data

    def update(self, instance, validated_data):
        fecha_dev = validated_data.get("fecha_devolucion")

        if fecha_dev and instance.fecha_devolucion is None:
            herramienta = Herramienta.objects.get(
                codigo=instance.herramienta_codigo
            )
            herramienta.estado = "disponible"
            herramienta.save()

        return super().update(instance, validated_data)
