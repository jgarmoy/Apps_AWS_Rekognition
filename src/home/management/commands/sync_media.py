from django.core.management.base import BaseCommand
from home.models import Imagen
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Sincroniza las imágenes de media/imagenes/ con la base de datos'

    def handle(self, *args, **kwargs):
        ruta = os.path.join(settings.MEDIA_ROOT, 'imagenes')
        for nombre in os.listdir(ruta):
            ruta_completa = os.path.join('imagenes', nombre)
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, ruta_completa)):
                if not Imagen.objects.filter(imagen=ruta_completa).exists():
                    Imagen.objects.create(imagen=ruta_completa)
                    self.stdout.write(self.style.SUCCESS(f'Añadida: {ruta_completa}'))
        self.stdout.write(self.style.SUCCESS('¡Sincronización completada!'))