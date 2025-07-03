from django.shortcuts import render, redirect
from django.http import Http404
from .forms import ImagenForm, ImagenesSelect
from lib_apps_aws_rekognition import apps_aws_rekognition as aar
from .models import Imagen
from django.conf import settings
import os

def mostrar_dir(request):

    directorios = os.listdir('./media')


    return render(request, 'mostrar_dir.html', {'directorios': directorios})

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
        if formulario.is_valid():
            formulario.save()
        return redirect('imagenes')
    else:

        return render(request, 'subir-imagen.html', {
            'form': ImagenForm()
        })
    
def ejercicios(request, numero_ejercicio):
    if numero_ejercicio < 1 or numero_ejercicio > 4:
        raise Http404('El ejercicio no existe.')
    
    if request.method == 'POST':
        formulario = ImagenesSelect(request.POST)
        if formulario.is_valid():
            request.session['imagen'] = formulario.cleaned_data['imagen']
            if numero_ejercicio == 4:
                return redirect("etiquetado_personas")

            return redirect(f"/mostrar/imagen/{numero_ejercicio}")
        else: 
            raise Http404('El formulario no es válido.')
        
    if numero_ejercicio == 1:
        texto = 'Difuminado de rostros.'
    elif numero_ejercicio == 2:
        texto = 'Difuminado de rostros solo a menores.'
    elif numero_ejercicio == 3:
        texto = 'Clasifica los rostros según sea menor, hombre o mujer.'
    else:
        texto = 'Etiquetado de rostros según sus nombres'


    return render(request, f"ejercicio.html", {
        'form': ImagenesSelect(),
        'texto': texto 
    })

def etiquetado_personas(request):
    
    if request.method == 'POST':
        # imagen: str = request.session['imagen']
        
        request.session["nombres"] = list(request.POST.values())[1:]

        return redirect(f"/mostrar/imagen/4")
    
    imagen: str = request.session['imagen']
    json_caras = aar.etiquetado_personas(imagen)

    return render(request, "nombrar-caras.html", {
        'caras': json_caras["caras"]
    })

def mostrar_imagen(request, numero_ejercicio):
    if numero_ejercicio < 1 or numero_ejercicio > 4:
        raise Http404('El ejercicio no existe')
    
    imagen: str = request.session['imagen']
    print(imagen)
    if numero_ejercicio == 1:
        img = aar.difuminado_rostros(imagen)
        texto = "Difuminado de rostros"
    elif numero_ejercicio == 2:
        img = aar.proteccion_menores(imagen)
        texto = "Difuminado de rostros de menores"
    elif numero_ejercicio == 3:
        img = aar.clasificacion_rostros(imagen)
        texto = "Clasificación de rostros"
    else:
        img = aar.nombrar_caras(imagen, request.session["nombres"])
        texto = "Etiquetado de personas"
        print(img)

    return render(request, "mostrar-imagen.html", {
        'imagen': f"/media/imagenes/creadas/{img}",
        "alt": texto
    })

def listar_imagenes(request):
    imagenes = Imagen.objects.all()
    return render(request, 'listar-iamgenes.html', {
        'imagenes': imagenes
    })


        
