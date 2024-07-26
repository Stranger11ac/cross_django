from django.contrib import admin
from . import models

class PreguntasAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'descripcion', 'fecha')
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutorial', 'blog_firma')
    search_fields = ('user__username', 'user__email')

# Register your models here.
admin.site.register(models.Mapa)
admin.site.register(models.Banners)
admin.site.register(models.Database)
admin.site.register(models.Articulos)
admin.site.register(models.Categorias)
admin.site.register(models.Notificacion)
admin.site.register(models.ImagenArticulo)
admin.site.register(models.Preguntas, PreguntasAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)

