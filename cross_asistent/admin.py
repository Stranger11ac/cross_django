from django.contrib import admin
from .models import proyectos, tareas, preguntas

# Register your models here.
admin.site.register(proyectos)
admin.site.register(tareas)
admin.site.register(preguntas)