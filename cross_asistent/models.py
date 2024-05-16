from django.db import models

# Create your models here.
class proyectos(models.Model):
    nombre = models.CharField(max_length=150)

class tareas(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(proyectos, on_delete=models.CASCADE)