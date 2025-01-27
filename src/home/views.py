from django.shortcuts import render, redirect
from django.http import Http404
from .forms import ImagenForm
from .models import Imagen

# Create your views here.
def inicio(request):
    return render(request, 'index.html', {})

def imagenes(request): 
    imagenes = Imagen.objects.all()
    return render(request, 'imagenes.html', {
        'imagenes': imagenes
    })

def subir_imagen(request):
    if request.method == 'POST':
        formulario = ImagenForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        print(formulario.is_valid())
        if formulario.is_valid():
            formulario.save()
        return redirect('imagenes')
    else:

        return render(request, 'subir-imagen.html', {
            'form': ImagenForm()
        })
    
def ejercicios(request, numero_ejercicio):
    if numero_ejercicio == 1:
        return render(request, 'ejercicio-1.html', {})
    elif numero_ejercicio == 2:
        return render(request, 'ejercicio-2.html', {})
    elif numero_ejercicio == 3:
        return render(request, 'ejercicio-3.html', {})
    elif numero_ejercicio == 4:
        return render(request, 'ejercicio-4.html')
    else:
        raise Http404('El ejercicio no existe')
    

