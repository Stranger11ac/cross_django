from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.dispatch import receiver
from django.conf import settings
from django.db import models
import os

"""Ruta de la imagen del Banner"""
def get_image_path(instance, filename):
    return os.path.join('cross_asistent/static/files/banners/', filename)

class Banners(models.Model):
    titulo = models.CharField(max_length=60, blank=False)
    descripcion = models.CharField(max_length=350, blank=False)
    articulo = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    expiracion = models.DateTimeField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = 'static/img/default_image.webp'
        else:
            if self.id:
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

"""Ruta de la imagen de Database segun la categoria"""
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
    documento = models.FileField(upload_to='cross_asistent/static/files/documentos/', blank=True, null=True)
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


"""Ruta de la imagen de los usuarios"""
def image_path_profile(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.user.username)}_perfil.{ext}"
    return os.path.join('cross_asistent/static/files/imagenes/personal', filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=image_path_profile, blank=True, null=True)
    tutorial = models.BooleanField(default=True)
    blog_firma = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Si se está actualizando la instancia y hay un cambio en la imagen de perfil
        if self.pk:
            old_profile = UserProfile.objects.get(pk=self.pk)
            if old_profile.profile_picture and old_profile.profile_picture != self.profile_picture:
                old_profile.profile_picture.delete(save=False)
        super(UserProfile, self).save(*args, **kwargs)

@receiver(post_delete, sender=UserProfile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)
