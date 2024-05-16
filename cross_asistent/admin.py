from django.contrib import admin
from . import models
# from .models import proyectos, tareas, preguntas

# Register your models here.
admin.site.register(models.banners)
admin.site.register(models.tareas)
admin.site.register(models.proyectos)
admin.site.register(models.preguntas)
admin.site.register(models.articulos)