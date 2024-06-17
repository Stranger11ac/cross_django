from django import forms
from django.forms import ModelForm
from .models import Tareas, Mapa, MapaImagenes

class crearTarea(ModelForm):
    class Meta:
        model = Tareas
        fields = ['tarea', 'importante']

class MapaForm(forms.ModelForm):
    class Meta:
        model = Mapa
        fields = ['lugar', 'informacion']

class MapaImagenesForm(forms.ModelForm):
    class Meta:
        model = MapaImagenes
        fields = ['imagen']

    imagen = forms.ImageField(widget=forms.ClearableFileInput())
