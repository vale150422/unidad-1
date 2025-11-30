from rest_framework import serializers
from api.models.herramienta import Herramienta


class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

