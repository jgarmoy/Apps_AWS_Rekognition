import os
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


