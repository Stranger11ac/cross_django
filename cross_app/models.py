from django.db import models

# Create your models here.
class proyectos(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class tareas(models.Model):
    title = models.CharField(max_length=150)
    descrption = models.TextField()
    project = models.ForeignKey(proyectos, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + " - " + self.project.name
    