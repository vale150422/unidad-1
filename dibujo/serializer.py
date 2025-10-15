from rest_framework import serializers
from.models import Dibujo

class DibujoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dibujo
        fields ='__all__'
        