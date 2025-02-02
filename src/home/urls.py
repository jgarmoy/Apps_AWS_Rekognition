from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('imagenes/', views.imagenes, name='imagenes'),
    path('subir-imagen/', views.subir_imagen, name='subir_imagen'),
    path('ejercicio/<int:numero_ejercicio>', views.ejercicios, name='ejercicio'),
    path('mostrar/imagen/<int:numero_ejercicio>', views.mostrar_imagen, name='mostrar_imagen'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)