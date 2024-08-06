from django.db.models.signals import pre_save, post_delete, pre_delete
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.dispatch import receiver
from django.conf import settings
from django.db import models
import random
import string
import os


"""Generar una cadena aleatoria"""
def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

"""Cambiar Nombre del Archivo"""
def create_filename_path(filename, setname, sufix,length, lenghtrandom, strpath):
    ext = filename.split('.')[-1]
    setname = setname[:length] if len(setname) > length else setname
    random_string = generate_random_string(lenghtrandom)
    filename = f"{sufix}_{slugify(setname)}_uid-{random_string}.{ext}"
    return os.path.join(strpath, filename)

"""Ruta imagen del Banner"""
def set_imgBanner_path(instance, filename):
    newName = instance.titulo.strip().replace(' ', '')
    thispath = 'cross_asistent/static/files/imagenes/banners/'
    return create_filename_path(filename, newName, 'banner', 15, 5, thispath)

"""Ruta imagen de Database segun categoria"""
def set_imgDB_path(instance, filename):
    newName = instance.titulo.strip().replace(' ', '')
    thispath = 'cross_asistent/static/files/imagenes/'
    if instance.categoria:
        categoria = instance.categoria.categoria
        if categoria == 'Mapa':
            thispath += 'mapa/'
        elif categoria == 'Calendario':
            thispath += 'calendario/'
    
    return create_filename_path(filename, newName, 'db', 20, 6, thispath)

"""Ruta imagen de Articulos"""
def set_imgBlog_path(instance, filename):
    newName = instance.titulo.strip().replace(' ', '')
    thispath = 'cross_asistent/static/files/imagenes/blogs/'
    return create_filename_path(filename, newName, 'blog', 18, 8, thispath)

"""Ruta imagenes"""
def set_imgs_path(instance, filename):
    newName = filename.strip().replace(' ', '')
    thispath = 'cross_asistent/static/files/imagenes/'
    return create_filename_path(filename, newName, 'cross_image', 20, 11, thispath)

"""Ruta imagen de perfiles"""
def set_imgProfile_path(instance, filename):
    newName = instance.user.username.strip().replace(' ', '')
    thispath = 'cross_asistent/static/files/imagenes/personal/'
    return create_filename_path(filename, newName, 'profile', 20, 8, thispath)

"""Ruta Documento de Database"""
def set_pdfDB_path(instance, filename):
    newName = instance.titulo.strip().replace(' ', '')
    thispath = 'cross_asistent/static/files/documentos/'
    return create_filename_path(filename, newName, 'db_doc', 18, 8, thispath)


class Banners(models.Model):
    titulo = models.CharField(max_length=150, null=True, blank=True)
    descripcion = models.CharField(max_length=350, null=True, blank=True)
    redirigir = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to=set_imgBanner_path, blank=True, null=True)
    expiracion = models.DateTimeField(blank=True, null=True)
    visible = models.BooleanField(default=True)
        
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = '/static/img/default_image.webp'
        else:
            if self.id:
                existing_banner = Banners.objects.get(id=self.id)
                if self.imagen != existing_banner.imagen:
                    existing_banner.imagen.delete(save=False)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.imagen:
            self.imagen.delete()
        super(Banners, self).delete(*args, **kwargs)

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
    muid = models.CharField(max_length=23)
    evento_fecha_inicio = models.DateTimeField(blank=True, null=True)
    evento_fecha_fin = models.DateTimeField(blank=True, null=True)
    evento_lugar = models.CharField(max_length=200, blank=True, null=True, default='Campus UTC')
    evento_className = models.CharField(max_length=100, blank=True, null=True, default='event_detail')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        if self.imagen:
            self.imagen.delete()
        if self.documento:
            self.documento.delete()
        super(Database, self).delete(*args, **kwargs)

class Articulos(models.Model):
    encabezado = models.ImageField(upload_to=set_imgBlog_path, blank=True, null=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    creacion = models.DateField(auto_now_add=True)
    actualizacion = models.DateField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
    def delete(self, *args, **kwargs):
        if self.encabezado:
            self.encabezado.delete()
        super(Articulos, self).delete(*args, **kwargs)

class Mapa(models.Model):
    muid = models.CharField(max_length=23)
    nombre = models.CharField(max_length=200)
    informacion = models.TextField()
    color = models.CharField(max_length=50)
    door_cords = models.CharField(max_length=100, null=True)
    p1_polygons = models.CharField(max_length=100, blank=True, null=True)
    p2_polygons = models.CharField(max_length=100, blank=True, null=True)
    p3_polygons = models.CharField(max_length=100, blank=True, null=True)
    p4_polygons = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Imagenes(models.Model):
    imagen = models.ImageField(upload_to=set_imgs_path, blank=True, null=True)
    
    def __str__(self):
        return self.imagen.name
    
    def delete(self, *args, **kwargs):
        if self.imagen:
            self.imagen.delete()
        super(Imagenes, self).delete(*args, **kwargs)

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


@receiver(pre_delete, sender=Banners)
def delete_files_on_object_delete(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(save=False)

@receiver(pre_delete, sender=Database)
def delete_files_on_object_delete(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(save=False)
    if instance.documento:
        instance.documento.delete(save=False)

@receiver(pre_delete, sender=Articulos)
def delete_files_on_object_delete(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(save=False)

@receiver(pre_delete, sender=Imagenes)
def delete_files_on_object_delete(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(save=False)

@receiver(post_delete, sender=UserProfile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)
