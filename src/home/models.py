from django.db import models

# Create your models here.
class Imagen(models.Model):
	json = models.FileField(upload_to='json/')
	imagen = models.ImageField(upload_to='imagenes/')
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		db_table = "imagenes"
		ordering = ['-created_at']