from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('imagenes/', views.imagenes, name='imagenes'),
]