from django.contrib import admin
from . import models
# from .models import proyectos, tareas, preguntas

class TareasProg(admin.ModelAdmin):
    readonly_fields = ('creacion',)

# Register your models here.
admin.site.register(models.Mapa)
admin.site.register(models.MapaImagenes)
admin.site.register(models.Banners)
admin.site.register(models.Database)
admin.site.register(models.Articulos)
admin.site.register(models.Categorias)
admin.site.register(models.Sugerencias_preg)
admin.site.register(models.Tareas, TareasProg)