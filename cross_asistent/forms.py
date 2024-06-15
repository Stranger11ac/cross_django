from django import forms
from django.forms import ModelForm
from .models import Tareas, Mapa, MapaImagenes
from .models import Database, Categorias

class crearTarea(ModelForm):
    class Meta:
        model = Tareas
        fields = ['tarea', 'importante']

class MapaForm(forms.ModelForm):
    class Meta:
        model = Mapa
        fields = ['lugar', 'descripcion']

class MapaImagenesForm(forms.ModelForm):
    class Meta:
        model = MapaImagenes
        fields = ['imagen']

    imagen = forms.ImageField(widget=forms.ClearableFileInput())

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Database
        fields = ['titulo']
    
    def save(self, commit=True):
        pregunta = super().save(commit=False)
        pregunta.categoria = Categorias.objects.get(categoria="Preguntas")
        if commit:
            pregunta.save()
        return pregunta