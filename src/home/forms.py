from django import forms
from .models import Imagen
from lib_apps_aws_rekognition.apps_aws_rekognition import get_imagenes

class ImagenForm(forms.ModelForm):
	class Meta:
		model = Imagen
		fields = ('json', 'imagen')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['json'].widget.attrs.update(
			{'accept': '.json'}
		)
		self.fields['imagen'].widget.attrs.update(
			{'accept': '.jpg, .jpeg, .png'}
		)
		self.fields['json'].required = False
		self.fields['imagen'].required = False

class ImagenesSelect(forms.Form):
	# imagen = forms.ChoiceField(choices=[("", "Elige una imagen ...")] + get_imagenes(), label='Selecciona una imagen') --> Esto no funciona correctamente, si subo una imagen nueva no me la carga hasta que no reinicio el servidor. Se ejecuta el get_imagenes() una vez cuando se carga y no se actualiza.
	imagen = forms.ChoiceField(choices=[], label='Selecciona una imagen')

	# De esta forma se carga dinámicamente con el constructor. Cada vez que se cree una instancia, Django llamará a __init__ y este ejecutará get_imagenes() para obtener las imágenes. 
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) # Llama al constructor original del formulario
		self.fields['imagen'].choices = [("", "Elige una imagen ...")] + get_imagenes()	

