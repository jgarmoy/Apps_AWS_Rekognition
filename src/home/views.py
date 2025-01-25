from django.shortcuts import render
from .forms import CrearImagen
from .models import Imagen
import os

# Create your views here.
def inicio(request):
    return render(request, 'index.html', {})

def imagenes(request): 
    imagenes = Imagen.objects.all()
    return render(request, 'imagenes.html', {
        'imagenes': imagenes
    })

def subir_imagen(request):
    if request.method == 'GET':
        return render(request, 'subir-imagen.html', {
            'form': CrearImagen()
        })
    else:
        # nombre = request.POST['nombre']
        # imagen = request.FILES['imagen']
        print(request.FILES['id_imagen'])
        # ruta_imagen = os.path.join('imagenes', 'subidas', nombre)
        # with (open(ruta_imagen, 'wb+')) as archivo:
        #     for chunk in imagen.chunks():
        #         archivo.write(chunk)
        return render(request, 'subir-imagen.html', {
        'imagen_subida': True
    })