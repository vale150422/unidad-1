from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views.prestamo_view import PrestamoViewSet
from api.views.herramienta_view import HerramientaViewSet
from api.views.busqueda_view import BusquedaView

router = DefaultRouter()
router.register(r'herramientas', HerramientaViewSet, basename='herramienta')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')

urlpatterns = [
    path("", include(router.urls)),              # ← mantiene /herramientas/ y /prestamos/
    path("buscar/", BusquedaView.as_view(), name="buscar"),
]

#genera automaticamente las urls para las vistas de herramientas y prestamos
#todo de manera defalult