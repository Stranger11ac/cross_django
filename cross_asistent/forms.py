from django.forms import ModelForm
from .models import Tareas

class crearTarea(ModelForm):
    class Meta:
        model = Tareas
        fields = ['tarea', 'importante']
