from django.contrib import admin
from . import models
# from .models import proyectos, tareas, preguntas

# Register your models here.
admin.site.register(models.Banners)
admin.site.register(models.Preguntas)
admin.site.register(models.Articulos)
admin.site.register(models.Sugerencias_preg)