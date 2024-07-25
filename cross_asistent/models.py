from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

def get_image_path(instance, filename):
    """Función para obtener la ruta de la imagen"""
    return os.path.join('cross_asistent/static/files/banners/', filename)

class Banners(models.Model):
    titulo = models.CharField(max_length=60, blank=False)
    descripcion = models.CharField(max_length=350, blank=False)
    articulo = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to=get_image_path, blank=True, null=True)  # Cambiado a opcional
    expiracion = models.DateTimeField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = 'static/img/default_image.webp'  # Asigna la imagen por defecto si no se proporciona una
        else:
            if self.id:
                # Obtener el banner existente
                existing_banner = Banners.objects.get(id=self.id)
                # Eliminar la imagen anterior si se actualiza
                if self.imagen != existing_banner.imagen:
                    existing_banner.imagen.delete(save=False)
        
        super(Banners, self).save(*args, **kwargs)

class Categorias(models.Model):
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    creacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.categoria

def get_image_upload_path(instance, filename):
    if instance.categoria and instance.categoria.categoria == 'Mapa':
        return os.path.join('cross_asistent/static/files/imagenes/mapa/', filename)
    elif instance.categoria and instance.categoria.categoria == 'Calendario':
        return os.path.join('cross_asistent/static/files/imagenes/calendario/', filename)
    else:
        return os.path.join('cross_asistent/static/files/imagenes/', filename)

class Database(models.Model):
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True)
    titulo = models.CharField(max_length=200, blank=False)
    informacion = models.TextField(blank=True, null=True)
    redirigir = models.URLField(blank=True, null=True)
    frecuencia = models.IntegerField(default=0)
    document = models.FileField(upload_to='cross_asistent/static/files/documentos/', blank=True, null=True)
    imagen = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    evento_fecha_inicio = models.DateTimeField(blank=True, null=True)
    evento_fecha_fin = models.DateTimeField(blank=True, null=True)
    evento_lugar = models.CharField(max_length=200, blank=True, null=True, default='Campus UTC')
    evento_className = models.CharField(max_length=100, default='event_detail')
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.titulo} - C: {self.categoria.categoria}'

class Articulos(models.Model):
    encabezado =  models.ImageField(upload_to='cross_asistent/static/files/imagenes/blogs/', blank=True, null=True)
    titulo = models.CharField(max_length=200, blank=False)
    contenido = models.TextField(blank=False)
    autor = models.CharField(max_length=100, blank=False)
    firma = models.CharField(max_length=150, blank=False)
    creacion = models.DateField(auto_now_add=True, blank=False)
    actualizacion = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.autor}"

class Mapa(models.Model):
    nombre = models.CharField(max_length=200, blank=False)
    informacion = models.TextField(null=False)
    color = models.CharField(max_length=50, null=False)
    door_cords = models.CharField(max_length=100, null=True)
    p1_polygons = models.CharField(max_length=100, blank=True, null=True)
    p2_polygons = models.CharField(max_length=100, blank=True, null=True)
    p3_polygons = models.CharField(max_length=100, blank=True, null=True)
    p4_polygons = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class ImagenArticulo(models.Model):
    imagen = models.ImageField(upload_to='cross_asistent/static/files/imagenes/blogs/imgs_blogs/', blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        # Eliminar la imagen del sistema de archivos al eliminar un registro
        if self.imagen:
            image_path = os.path.join(settings.MEDIA_ROOT, self.imagen.path)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super(Banners, self).delete(*args, **kwargs)

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tipo} - {self.mensaje}'

class Preguntas(models.Model):
    pregunta = models.CharField(max_length=150, blank=False)
    descripcion = models.TextField(null=False, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pregunta
