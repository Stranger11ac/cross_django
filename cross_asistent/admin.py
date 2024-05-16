from django.contrib import admin
# from .models import proyectos, tareas, preguntas
from . import models

# Register your models here.
admin.site.register(models.proyectos)
admin.site.register(models.tareas)
admin.site.register(models.preguntas)