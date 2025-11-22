from rest_framework.response import Response
from rest_framework.views import APIView
from project.serializers.clase_serializer import ClaseSerializers
from api.models.clase import Clase
from rest_framework import status
from django.http import Http404

class Clase_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        queryset = Clase.objects.all()
        numero_clase = self.request.query_params.get('numero_clase')
        if numero_clase is not None:
            queryset =queryset.filter(numero_clase=numero_clase)
        serializer = ClaseSerializers(queryset, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ClaseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Clase_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Clase.objects.get(pk=pk)
        except Clase.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ClaseSerializers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ClaseSerializers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)