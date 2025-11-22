from rest_framework import serializers
from api.models.clase import Clase

class ClaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clase
        exclude = ['fecha']
        