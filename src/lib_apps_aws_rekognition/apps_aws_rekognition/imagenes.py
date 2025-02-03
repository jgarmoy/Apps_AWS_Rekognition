## CASO PRÁCTICO: DISEÑO DE APPS CON AWS REKOGNITION

# Importación de librerias
import cv2
import numpy as np
from home.models import Imagen
import os
import json
from typing import List
from django.conf import settings

def get_imagenes():
    """
    Obtener las iamgenes de la carperta media/imagenes
    """
    ruta_imagenes = os.path.join(settings.MEDIA_ROOT, 'imagenes')
    try:
        imagenes = [(img, img) for img in os.listdir(ruta_imagenes) if img.endswith(('.jpg', '.jpeg', '.png'))]
    except FileNotFoundError:
        imagenes = []
        
    return imagenes


def guardar_imagen(nombre_imagen: str, imagen: np.ndarray):
    """
    Guarda una imagen en el directorio imagenes/creadas.

    Args:
        nombre_imagen (str): Nombre con el que se guardará la imagen, incluyendo su extensión.
        imagen (np.ndarray): Imagen que se desea guardar.

    Returns:
        None
    """
    cv2.imwrite(nombre_imagen, imagen)
    print("Imagen guardada en el directorio creadas")

def formatear_ruta(directorios: List, nombre_imagen: str) -> str:
    """
    Formatea la ruta de la imagen.

    Args:
        directorios (List): Lista con los directorios donde se encuentra la imagen.

    Returns:
        np.ndarray: Imagen procesada (arreglo de NumPy).
    """
    return os.path.join(*directorios, nombre_imagen)

def formatear_nombre_imagen(nombre_imagen: str, texto: str) -> str:
    """
    Formatea el nombre de una imagen agregando un texto adicional antes de la extensión.

    Args:
        nombre_imagen (str): Nombre original de la imagen, incluyendo su extensión.
        texto (str): Texto que se agregará al nombre de la imagen.

    Returns:
        str: Nombre formateado de la imagen.
    """
    return f"{nombre_imagen.split('.')[0]}{texto}.{nombre_imagen.split('.')[1]}"

def calcular_cuadrado(imagen):
    pass



#############################################################
## 1. Caso práctico uno: difuminado de rostros
def difuminado_rostros(nombre_imagen: str):
    
    imagen_db = Imagen.objects.get(imagen=formatear_ruta(["imagenes"], nombre_imagen))

    imagen_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.imagen))
    json_ruta = formatear_ruta([settings.MEDIA_ROOT], imagen_db.json.__str__())

    try:
        with open(json_ruta, "r") as archivo:
            imagen_json = json.load(archivo)
    except FileNotFoundError:
        print("El fichero no se ha encontrado") # Este error no debería de ocurrir nunca
    except json.JSONDecodeError:
        print("Ha ocurrido un error al decodificar el json")

    
    imagen = cv2.imread(imagen_ruta, cv2.IMREAD_UNCHANGED)

    if imagen is None:
        raise FileNotFoundError("La imagen no se ha encontrado")

    alto, ancho = imagen.shape[:2]

    for cara in imagen_json["FaceDetails"]:
        ancho_cara = float(cara["BoundingBox"]["Width"])
        alto_cara = float(cara["BoundingBox"]["Height"])
        esquina_izquierda = float(cara["BoundingBox"]["Left"])
        esquina_superior = float(cara["BoundingBox"]["Top"])
        x1, y1 = round(esquina_izquierda * ancho), round(esquina_superior * alto)
        x2, y2 = round(x1 + ancho_cara * ancho), round(y1 + alto_cara * alto)

        imagen[y1:y2, x1:x2] = cv2.medianBlur(imagen[y1:y2, x1:x2], 99)


    nombre_nueva_imagen = formatear_ruta([settings.MEDIA_ROOT, "imagenes", "creadas"], formatear_nombre_imagen(nombre_imagen, "_dif"))
    print(nombre_nueva_imagen)
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    return os.path.split(nombre_nueva_imagen)[1]

    





#############################################################
## 2. Caso práctico dos: protección de menores
def proteccion_menores(nombre_imagen: str):
    imagen_db = Imagen.objects.get(imagen=formatear_ruta(["imagenes"], nombre_imagen))

    imagen_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.imagen))
    json_ruta = formatear_ruta([settings.MEDIA_ROOT], imagen_db.json.__str__())

    try:
        with open(json_ruta, "r") as archivo:
            imagen_json = json.load(archivo)
    except FileNotFoundError:
        print("El fichero no se ha encontrado") # Este error no debería de ocurrir nunca
    except json.JSONDecodeError:
        print("Ha ocurrido un error al decodificar el json")

    
    imagen = cv2.imread(imagen_ruta, cv2.IMREAD_UNCHANGED)

    if imagen is None:
        raise FileNotFoundError("La imagen no se ha encontrado")

    alto, ancho = imagen.shape[:2]

    for cara in imagen_json["FaceDetails"]:
        if cara["AgeRange"]["Low"] < 18:
            ancho_cara = float(cara["BoundingBox"]["Width"])
            alto_cara = float(cara["BoundingBox"]["Height"])
            esquina_izquierda = float(cara["BoundingBox"]["Left"])
            esquina_superior = float(cara["BoundingBox"]["Top"])
            x1, y1 = round(esquina_izquierda * ancho), round(esquina_superior * alto)
            x2, y2 = round(x1 + ancho_cara * ancho), round(y1 + alto_cara * alto)

            imagen[y1:y2, x1:x2] = cv2.medianBlur(imagen[y1:y2, x1:x2], 99)


    nombre_nueva_imagen = formatear_ruta([settings.MEDIA_ROOT, "imagenes", "creadas"], formatear_nombre_imagen(nombre_imagen, "_dif_men"))
    print(nombre_nueva_imagen)
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    return os.path.split(nombre_nueva_imagen)[1]


#############################################################
## 3. Caso práctico tres: clasificación de rostros
def clasificacion_rostros():
    pass


#############################################################
## 4. Caso práctico cuatro: etiquetado de personas
def etiquetado_personas():
    pass
