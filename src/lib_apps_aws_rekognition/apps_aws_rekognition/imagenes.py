## CASO PRÁCTICO: DISEÑO DE APPS CON AWS REKOGNITION

# Importación de librerias
import cv2
import numpy as np
from home.models import Imagen
import os
import json
from typing import List
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

AMARILLO = (0, 255, 255)
ROJO = (0, 0, 255)
VERDE = (0, 255, 0)

def get_imagenes():
    imagenes = Imagen.objects.all()
    opciones = []
    for img in imagenes:
        nombre_archivo = os.path.split(img.imagen.name)[1]
        ruta_completa = os.path.join(settings.MEDIA_ROOT, img.imagen.name)
        if os.path.exists(ruta_completa):
            opciones.append((nombre_archivo, nombre_archivo))
    return opciones



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

def eliminar_ficheros_etiquetado():
    """
    Elimina las imagenes que tenga el directorio /media/imagenes/etiquetadoPersonas
    """
    lista_ficheros = os.listdir(formatear_ruta([settings.MEDIA_ROOT, "imagenes"], "etiquetadoPersonas"))

    for fichero in lista_ficheros:
        os.remove(formatear_ruta([settings.MEDIA_ROOT, "imagenes", "etiquetadoPersonas"], fichero))



#############################################################
## 1. Caso práctico uno: difuminado de rostros
def difuminado_rostros(nombre_imagen: str) -> str:
    """
    Difumina los rotros a partir de un JSON y guarda la imagen generada.
    Args:
        nombre_imagen (str): Nombre original de la imagen, incluyendo su extensión.
    
    Returns:
        str: Nombre de la imagen generada.
    """
    
    try:
        imagen_db = Imagen.objects.get(imagen__endswith=nombre_imagen)
    except ObjectDoesNotExist:
        raise FileNotFoundError(f"No se encontró una imagen que termine en: {nombre_imagen}")

    imagen_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.imagen))
    json_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.json))

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
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    return os.path.split(nombre_nueva_imagen)[1]

    





#############################################################
## 2. Caso práctico dos: protección de menores
def proteccion_menores(nombre_imagen: str) -> str:
    """
    Difumina los rotros solo de los menores a partir de un JSON y guarda la imagen generada.
    Args:
        nombre_imagen (str): Nombre original de la imagen, incluyendo su extensión.
    
    Returns:
        str: Nombre de la imagen generada.
    """
    try:
        imagen_db = Imagen.objects.get(imagen__endswith=nombre_imagen)
    except ObjectDoesNotExist:
        raise FileNotFoundError(f"No se encontró una imagen que termine en: {nombre_imagen}")

    imagen_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.imagen))
    json_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.json))

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
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    return os.path.split(nombre_nueva_imagen)[1]


#############################################################
## 3. Caso práctico tres: clasificación de rostros
def clasificacion_rostros(nombre_imagen: str) -> str:
    """
    Clasifica los rostros a partir de un JSON y guarda la imagen generada.
    Args:
        nombre_imagen (str): Nombre original de la imagen, incluyendo su extensión.
    
    Returns:
        str: Nombre de la imagen generada.
    """
    try:
        imagen_db = Imagen.objects.get(imagen__endswith=nombre_imagen)
    except ObjectDoesNotExist:
        raise FileNotFoundError(f"No se encontró una imagen que termine en: {nombre_imagen}")

    imagen_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.imagen))
    json_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.json))

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

        if cara["AgeRange"]["Low"] < 18:
            cv2.rectangle(imagen, (x1, y1), (x2, y2), AMARILLO)

        elif cara["Gender"]["Value"] == "Male":
            cv2.rectangle(imagen, (x1, y1), (x2, y2), ROJO)
        else: 
            cv2.rectangle(imagen, (x1, y1), (x2, y2), VERDE)

        emociones = cara["Emotions"]

        texto = f"{emociones[0]["Type"]}:{emociones[0]["Confidence"]:.2f}"

        (texto_ancho, texto_alto), baseline = cv2.getTextSize(texto, 0, 0.5, 1)

        escala_w = (x2 - x1) / texto_ancho
        escala = escala_w * 0.5

        cv2.putText(imagen, texto, (x1 + 1, y2 - 5), 0, escala, (0, 0, 0), 1, cv2.LINE_AA)


    nombre_nueva_imagen = formatear_ruta([settings.MEDIA_ROOT, "imagenes", "creadas"], formatear_nombre_imagen(nombre_imagen, "_dif_men"))
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    return os.path.split(nombre_nueva_imagen)[1]


#############################################################
## 4. Caso práctico cuatro: etiquetado de personas
def etiquetado_personas(nombre_imagen: str):
    """
    Etiqueta los rotros a partir de un JSON y pide los nombres de los rostros detectados.
    Args:
        nombre_imagen (str): Nombre original de la imagen, incluyendo su extensión.
    
    Returns:
        Dict: Diccionario con los datos de las caras obtenidas a partir del JSON.
    """
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

    eliminar_ficheros_etiquetado()

    nuevo_json = {
        "imagen_original": nombre_imagen,
        "cantidad_rostros_detectados": len(imagen_json["FaceDetails"])
    }

    alto, ancho = imagen.shape[:2]
    caras_json = []

    for (indice, cara) in enumerate(imagen_json["FaceDetails"]):
        ancho_cara = float(cara["BoundingBox"]["Width"])
        alto_cara = float(cara["BoundingBox"]["Height"])
        esquina_izquierda = float(cara["BoundingBox"]["Left"])
        esquina_superior = float(cara["BoundingBox"]["Top"])
        x1, y1 = round(esquina_izquierda * ancho), round(esquina_superior * alto)
        x2, y2 = round(x1 + ancho_cara * ancho), round(y1 + alto_cara * alto)

        guardar_imagen(formatear_ruta([settings.MEDIA_ROOT, "imagenes", "etiquetadoPersonas"], f"{indice}.jpg"), imagen[y1:y2, x1:x2])


        cara_json = {
            "id": indice,
            "nombre": "",
            "edad": cara["AgeRange"]["Low"],
            "sexo": cara["Gender"]["Value"],
            "posicion": {
                "punto1": [x1, y1],
                "punto2": [x2, y2]
            },
            "emociones": cara["Emotions"],
            "sonriendo": cara["Smile"]["Value"],
            "img": f"{formatear_ruta([settings.MEDIA_URL, "imagenes", "etiquetadoPersonas"], f"{indice}.jpg")}",
            "alt": f"Cara {indice}"
        }
        caras_json.append(cara_json)

    nuevo_json["caras"] = caras_json
        
    nuevo_json_ruta = formatear_ruta([settings.MEDIA_ROOT, "json", "etiquetadoPersonas"], f"{nombre_imagen.split(".")[0]}.json")

    try:
        with open(nuevo_json_ruta, "w") as archivo:
            json.dump(nuevo_json, archivo, indent = 4)
    except FileNotFoundError:
        print("El fichero no se ha encontrado") # Este error no debería de ocurrir nunca
    except json.JSONDecodeError:
        print("Ha ocurrido un error al decodificar el json")

    return nuevo_json

def nombrar_caras(nombre_imagen: str, nombres: List) -> str:
    """
    Marca con un rectángulo el rostro, le añade el nombre y guarda la imagen resultante.
    Args:
        nombre_imagen (str): Nombre original de la imagen, incluyendo su extensión.
        nombres (List): Lista con los nombres.
    
    Returns:
        str: Nombre de la imagen generada.
    """
    imagen_db = Imagen.objects.get(imagen=formatear_ruta(["imagenes"], nombre_imagen))
    imagen_ruta = formatear_ruta([settings.MEDIA_ROOT], str(imagen_db.imagen))
    json_ruta = formatear_ruta([settings.MEDIA_ROOT, "json", "etiquetadoPersonas"], f"{nombre_imagen.split(".")[0]}.json")


    try:
        with open(json_ruta, "r") as archivo:
            json_caras = json.load(archivo)
    except FileNotFoundError:
        print("El fichero no se ha encontrado") # Este error no debería de ocurrir nunca
    except json.JSONDecodeError:
        print("Ha ocurrido un error al decodificar el json")

    for (indice, nombre) in enumerate(nombres):
        json_caras["caras"][indice]["nombre"] = nombre

    

    imagen = cv2.imread(imagen_ruta, cv2.IMREAD_UNCHANGED)

    if imagen is None:
        raise FileNotFoundError("La imagen no se ha encontrado")
    
    for cara in json_caras["caras"]:
        # punto1 = (int(num) for num in cara["posicion"]["punto1"])
        punto1 = cara["posicion"]["punto1"]
        punto2 = cara["posicion"]["punto2"] 
        nombre = cara["nombre"]
        cv2.rectangle(imagen, punto1, punto2, (0, 0, 255))

        (texto_ancho, texto_alto), baseline = cv2.getTextSize(nombre, 0, 0.5, 1)

        escala_w = (punto2[0] - punto1[0]) / texto_ancho
        escala = escala_w * 0.5

        cv2.putText(imagen, nombre, (punto1[0] + 1, punto2[1] - 5), 0, escala, (0, 0, 0), 1, cv2.LINE_AA)
        

    nombre_nueva_imagen = formatear_ruta([settings.MEDIA_ROOT, "imagenes", "creadas"], formatear_nombre_imagen(nombre_imagen, "_eti_per"))

    nuevo_json_ruta = formatear_ruta([settings.MEDIA_ROOT, "json", "etiquetadoPersonas"], f"{nombre_imagen.split(".")[0]}.json")

    try:
        with open(nuevo_json_ruta, "w") as archivo:
            json.dump(json_caras, archivo, indent = 4)
    except FileNotFoundError:
        print("El fichero no se ha encontrado") # Este error no debería de ocurrir nunca
    except json.JSONDecodeError:
        print("Ha ocurrido un error al decodificar el json")
    
    guardar_imagen(nombre_nueva_imagen, imagen)

    return os.path.split(nombre_nueva_imagen)[1]