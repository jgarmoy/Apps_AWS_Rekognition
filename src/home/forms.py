from django import forms

class CrearImagen (forms.Form):
    nombre = forms.CharField(label="Nombre de la imagen y terminación",max_length=50, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    imagen = forms.ImageField(label="Imagen")