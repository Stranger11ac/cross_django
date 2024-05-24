from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class Preguntas(models.Model):
    pregunta = models.CharField(max_length=200, blank=False)
    respuesta = models.TextField(blank=True, null=True)
    redirigir = models.URLField(blank=True, null=True)
    documentos = models.FileField(upload_to='cross_asistent/static/files/documentos/', blank=True, null=True)
    imagenes =  models.ImageField(upload_to='cross_asistent/static/files/imagenes/', blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.pregunta

class Sugerencias_preg(models.Model):
    pregunta_num = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    sugerencia = models.TextField()
    sugerente = models.CharField(max_length=100, default='Anonimo')
    
    def __str__(self):
        return f"pregunta #:{self.pregunta_num.id} sugiere: {self.sugerente}"

class Articulos(models.Model):
    creacion = models.DateField(auto_now_add=True, blank=False)
    actualizacion = models.DateField(auto_now=True, blank=True, null=True)
    titulo = models.CharField(max_length=200, blank=False)
    contenido = models.TextField(blank=False)
    Encabezado =  models.ImageField(upload_to='cross_asistent/static/files/imagenes/', blank=True, null=True)
    autor = models.CharField(max_length=150, blank=False)
    
    def __str__(self):
        return f"{self.titulo} - {self.autor}"

class Banners(models.Model):
    titulo = models.CharField(max_length=40, blank=False)
    descripcion = models.CharField(max_length=350, blank=False)
    articulo = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to='cross_asistent/static/files/banners/', blank=False)
    expiracion = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        # Eliminar la imagen del sistema de archivos al eliminar un registro
        if self.imagen:
            image_path = os.path.join(settings.MEDIA_ROOT, self.imagen.path)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super(Banners, self).delete(*args, **kwargs)

class Tareas(models.Model):
    tarea = models.CharField(max_length=255)
    importante = models.BooleanField(default=False)
    creacion = models.DateTimeField(auto_now_add=True)
    completar = models.BooleanField(default=False)
    completado_fecha = models.DateTimeField(null=True, blank=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.tarea} - de:{self.propietario.username}"
