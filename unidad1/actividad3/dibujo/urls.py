from django.urls import path, include
from rest_framework.routers import DefaultRouter
from.views import DibujosViewSet

router = DefaultRouter()
router.register(r'dibujos', DibujosViewSet)

urlpatterns = [

    path('', include (router.urls)),
]