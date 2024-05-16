from django.db import models

# Create your models here.
class proyectos(models.Model):
    nombre = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nombre

class tareas(models.Model):
    proyecto = models.ForeignKey(proyectos, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.titulo + " - " + self.proyecto.nombre