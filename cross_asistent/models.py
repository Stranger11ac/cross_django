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
    redirigir = models.URLField(blank=True, null=True)
    documentos = models.FileField(upload_to='referencias/documentos/', blank=True, null=True)
    imagenes =  models.ImageField(upload_to='referencias/imagenes/', blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.pregunta
    
class articulos(models.Model):
    creacion = models.DateField(auto_now_add=True, blank=False)
    actualizacion = models.DateField(auto_now=True, blank=True, null=True)
    titulo = models.CharField(max_length=200, blank=False)
    contenido = models.TextField(blank=False)
    autor = models.CharField(max_length=150, blank=False)
    
    def __str__(self):
        return self.titulo + " - " + self.autor

class banners(models.Model):
    titulo = models.CharField(max_length=150, blank=False)
    descripcion = models.CharField(max_length=200, blank=False)
    articulo = models.URLField(blank=False, default=False)
    imagen = models.ImageField(upload_to='referencias/banners', blank=False)
    expiracion = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo