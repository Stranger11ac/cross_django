from django.contrib import admin
from . import models
# from .models import proyectos, tareas, preguntas
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class TareasProg(admin.ModelAdmin):
    readonly_fields = ('creacion',)

# Register your models here.
admin.site.register(models.Mapa)
admin.site.register(models.Banners)
admin.site.register(models.Database)
admin.site.register(models.Articulos)
admin.site.register(models.Categorias)
admin.site.register(models.ImagenArticulo)
admin.site.register(models.Sugerencias_preg)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image', 'is_online')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)