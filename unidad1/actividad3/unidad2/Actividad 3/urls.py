from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_Dibujo, name='lista_Dibujo'),
    path('crear/', views.crear_Dibujo, name='crear_Dibujo'),
    path('eliminar/<int:moto_id>/', views.eliminar_Dibujo, name='eliminar_Dubujo'),
]
