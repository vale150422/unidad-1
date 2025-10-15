from rest_framework import viewsets
from .models import Dibujo
from .serializer import DibujoSerializer

class DibujosViewSet(viewsets.ModelViewSet):
    queryset = Dibujo.objects.all()
    serializer_class = DibujoSerializer






    

    
