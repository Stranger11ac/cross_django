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

class preguntas(models.Model):
    pregunta = models.CharField(max_length=200, blank=False)
    respuesta = models.TextField(blank=False)
    redirigir = models.URLField(blank=True)
    documentos = models.FileField(upload_to='referencias/documentos/', blank=True)
    imagenes =  models.ImageField(upload_to='referencias/imagenes/', blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.pregunta

class banners(models.Model):
    titulo = models.CharField(max_length=150, blank=False)
    descripcion = models.CharField(max_length=200, blank=False)
    imagen = models.ImageField(upload_to='referencias/banners', blank=False)
    expiracion = models.DateTimeField(blank=True)