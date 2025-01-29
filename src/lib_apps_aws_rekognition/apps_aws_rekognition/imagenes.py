## CASO PRÁCTICO: DISEÑO DE APPS CON AWS REKOGNITION

# Importación de librerias
import cv2
import numpy as np
import os
import json
from typing import List
from django.conf import settings


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

    nombre_img = os.path.split(nombre_imagen)[1] # Devuelve la cola de la ruta, es decir, el fichero. Si ponemos 0 nos devuelve el resto de la ruta. Si la ruta es todo directorios el 1 está vacío

    ruta = os.path.join(settings.MEDIA_ROOT, "json", nombre_imagen)

    try:
        with open(ruta, "r") as archivo:
            imagen_json = json.load(archivo)
    except FileNotFoundError:
        print("El fichero no se ha encontrado") # Este error no debería de ocurrir nunca
    except json.JSONDecodeError:
        print("Ha ocurrido un error al decodificar el json")

    
    imagen = cv2.imread(nombre_imagen, cv2.IMREAD_UNCHANGED)

    medidas_cuadrado = imagen["FaceDetails"]

    face_

    alto, ancho = imagen.shape[:2]



    zona_borrosa = "poner la parte de la imagen que tengo que emborronar"

    img_emborronada =  cv2.medianBlur(zona_borrosa, 99)



    nombre_nueva_imagen = formatear_ruta(["imagenes", "creadas"], formatear_nombre_imagen(nombre_imagen, "_dif"))
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    





#############################################################
## 2. Caso práctico dos: protección de menores
def proteccion_menores():
    pass


#############################################################
## 3. Caso práctico tres: clasificación de rostros
def clasificacion_rostros():
    pass


#############################################################
## 4. Caso práctico cuatro: etiquetado de personas
def etiquetado_personas():
    pass