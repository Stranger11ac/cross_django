from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.dispatch import receiver
from django.conf import settings
import random
import string
import os


"""Generar una cadena aleatoria"""
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


"""Ruta imagen del Banner"""
def set_imgBanner_path(instance, filename):
    ext = filename.split('.')[-1]
    newName = instance.titulo.strip().replace(' ', '')
    newName = newName[:15] if len(newName) > 15 else newName
    filename = f"banner_{slugify(newName)}.{ext}"
    return os.path.join('cross_asistent/static/files/imagenes/banners/', filename)

"""Ruta imagen de Database segun categoria"""
def set_imgDB_path(instance, filename):
    ext = filename.split('.')[-1]
    newName = instance.titulo.strip().replace(' ', '')
    newName = newName[:20] if len(newName) > 20 else newName
    filename = f"db_{slugify(newName)}.{ext}"
    
    if instance.categoria and instance.categoria.categoria == 'Mapa':
        return os.path.join('cross_asistent/static/files/imagenes/mapa/', filename)
    elif instance.categoria and instance.categoria.categoria == 'Calendario':
        return os.path.join('cross_asistent/static/files/imagenes/calendario/', filename)
    else:
        return os.path.join('cross_asistent/static/files/imagenes/', filename)

"""Ruta imagen de Articulos"""
def set_imgBlog_path(instance, filename):
    ext = filename.split('.')[-1]
    newName = instance.titulo.strip().replace(' ', '')
    newName = newName[:18] if len(newName) > 18 else newName
    random_string = generate_random_string(8)
    filename = f"blog_{slugify(newName)}_uid-{random_string}.{ext}"
    return os.path.join('cross_asistent/static/files/imagenes/blogs/', filename)

"""Ruta imagenes"""
def set_imgs_path(instance, filename):
    ext = filename.split('.')[-1]
    random_string = generate_random_string(12)
    filename = f"cross_{random_string}_img.{ext}"
    return os.path.join('cross_asistent/static/files/imagenes/', filename)

"""Ruta imagen de perfiles"""
def set_imgProfile_path(instance, filename):
    ext = filename.split('.')[-1]
    newName = instance.user.username.strip().replace(' ', '')
    newName = newName[:20] if len(newName) > 20 else newName
    random_string = generate_random_string(8)
    filename = f"profile_{slugify(newName)}_uid-{random_string}.{ext}"
    return os.path.join('cross_asistent/static/files/imagenes/personal', filename)

"""Ruta Documento de Database"""
def set_pdfDB_path(instance, filename):
    ext = filename.split('.')[-1]
    newName = instance.titulo.strip().replace(' ', '')
    newName = newName[:18] if len(newName) > 18 else newName
    random_string = generate_random_string(8)
    filename = f"db_pdf_{slugify(newName)}_uid-{random_string}.{ext}"
    return os.path.join('cross_asistent/static/files/documentos/', filename)

class Banners(models.Model):
    titulo = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=350)
    redirigir = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to=set_imgBanner_path, blank=True, null=True)
    expiracion = models.DateTimeField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = '/static/img/default_image.webp'
        else:
            if self.id:
                existing_banner = Banners.objects.get(id=self.id)
                if self.imagen != existing_banner.imagen:
                    existing_banner.imagen.delete(save=False)
        super().save(*args, **kwargs)

class Categorias(models.Model):
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    creacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.categoria    

class Database(models.Model):
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True)
    titulo = models.CharField(max_length=200)
    informacion = models.TextField(blank=True, null=True)
    redirigir = models.URLField(blank=True, null=True)
    frecuencia = models.IntegerField(default=0)
    documento = models.FileField(upload_to=set_pdfDB_path, blank=True, null=True)
    imagen = models.ImageField(upload_to=set_imgDB_path, blank=True, null=True)
    evento_fecha_inicio = models.DateTimeField(blank=True, null=True)
    evento_fecha_fin = models.DateTimeField(blank=True, null=True)
    evento_lugar = models.CharField(max_length=200, blank=True, null=True, default='Campus UTC')
    evento_className = models.CharField(max_length=100, blank=True, null=True, default='event_detail')
    fecha_modificacion = models.DateTimeField(auto_now=True)

class Articulos(models.Model):
    encabezado = models.ImageField(upload_to=set_imgBlog_path, blank=True, null=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    creacion = models.DateField(auto_now_add=True)
    actualizacion = models.DateField(auto_now=True, blank=True, null=True)

class Mapa(models.Model):
    nombre = models.CharField(max_length=200)
    informacion = models.TextField()
    color = models.CharField(max_length=50)
    door_cords = models.CharField(max_length=100, null=True)
    p1_polygons = models.CharField(max_length=100, blank=True, null=True)
    p2_polygons = models.CharField(max_length=100, blank=True, null=True)
    p3_polygons = models.CharField(max_length=100, blank=True, null=True)
    p4_polygons = models.CharField(max_length=100, blank=True, null=True)

class Imagenes(models.Model):
    imagen = models.ImageField(upload_to=set_imgs_path, blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        if self.imagen:
            image_path = os.path.join(settings.MEDIA_ROOT, self.imagen.path)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

class Preguntas(models.Model):
    pregunta = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=set_imgProfile_path, blank=True, null=True)
    tutorial = models.BooleanField(default=True)
    blog_firma = models.TextField(blank=True, null=True)
    password_update = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_profile = UserProfile.objects.get(pk=self.pk)
            if old_profile.profile_picture and old_profile.profile_picture != self.profile_picture:
                old_profile.profile_picture.delete(save=False)
        super().save(*args, **kwargs)

@receiver(post_delete, sender=UserProfile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)
