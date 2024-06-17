from django import forms
from django.forms import ModelForm
from .models import Tareas
from .models import Database, Categorias

class crearTarea(ModelForm):
    class Meta:
        model = Tareas
        fields = ['tarea', 'importante']

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