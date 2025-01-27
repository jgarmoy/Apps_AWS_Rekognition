from django import forms
from .models import Imagen

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
