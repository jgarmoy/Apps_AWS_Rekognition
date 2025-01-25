from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('imagenes/', views.imagenes, name='imagenes'),
    path('subir-imagen/', views.subir_imagen, name='subir_imagen'),
]