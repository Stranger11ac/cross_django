from django.urls import path
from . import functions, views, imex_port

urlpatterns = [
    # Páginas de inicio ----------------------------------------------------------
    path('', views.index, name='home'),
    path('chatbot/', functions.chatbot, name='chatbot'),
    path('preguntas_frecuentes/', views.faq, name='faq'),
    path('preguntar/', views.crear_pregunta, name='enviar_preguntas'),
    path('blogs/', views.blogs, name='blog'),
    path('blogs/<int:Articulos_id>/', views.mostrar_blog, name='mostrar_blog'),
    path('calendario/', views.calendario, name='calendario'),
    path('calendario/eventos/', functions.calendario_eventos, name='calendario_eventos'),
    path('mapa/', views.map, name='map'),
    path('mapa/edificios/', functions.mapa_data, name='mapa_edificios'),
    path('acercade/', views.about, name='about'),
    
    # Sesion y registro ----------------------------------------------------------
    path('logout/', views.singout, name='singout'),
    path('acceder/', views.singinpage, name='singin'),
    path('registro/', views.singup, name='singup'),
    
    # Administracion y programacion ----------------------------------------------------------
    path('administracion/', views.vista_admin, name='vista_admin'),
    path('administracion/programador/', views.vista_programador, name='vista_programador'),
    path('administracion/perfil/', views.ver_perfil, name='perfil'),
    path('administracion/perfil/editar_perfil', functions.editar_perfil, name='editprofile'),
    
    # Usuarios ----------------------------------------------------------
    path('administracion/modificar_usuario/', functions.in_active, name='in_active'),
    path('administracion/editar_usuario/<int:user_id>/', functions.editar_usuario, name='editar_usuario'),
    path('administracion/eliminar_usuario/<int:user_id>/', functions.eliminar_usuario, name='eliminar_usuario'),
    path('administracion/Database/', functions.createDatabase, name='create_database'),
    
    # Banners ----------------------------------------------------------
    path('administracion/banners/', views.upload_banner, name='upload_banner'),
    path('administracion/banners/<int:banner_id>/edit/', views.edit_banner, name='edit_banner'),
    path('administracion/banners/delete/<int:banner_id>/', views.delete_banner, name='delete_banner'),
    path('administracion/update_banner_visibility/', functions.update_banner_visibility, name='update_banner_visibility'),

    # Database ----------------------------------------------------------
    path('administracion/Base_de_datos/', views.database_page, name='database_page'),

    # Blog ----------------------------------------------------------
    path('administracion/crear_blog/', views.create_blog, name='create_blog'),
    path('administracion/subir_img_blog/', views.upload_image, name='send_imgsblog'),
    path('administracion/lista_imagenes/', views.lista_imagenes, name='lista_imagenes'),
    
    # Mapa ----------------------------------------------------------
    path('administracion/mapa/', views.update_mapa, name='update_mapa'),
    path('administracion/subir_mapa/', views.update_create_pleace_map, name='regEdificio'),
    
    # Notificaciones ----------------------------------------------------------
    path('administracion/notificaciones/', views.ver_notis, name='notificaciones'),
    path('administracion/notificacion_leida/', views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),

    # Preguntas ----------------------------------------------------------
    path('administracion/pregunta_eliminar/', functions.preguntas_deleted, name='question_deleted'),
    
    # Importar y Exportar ----------------------------------------------------------
    path('administracion/export/categorias/', imex_port.export_categorias, name='export_categorias'),
    path('administracion/importar/categorias/', imex_port.import_categorias, name='import_categorias'),
    path('administracion/export/database/', imex_port.export_database, name='export_database'),
    path('administracion/importar/database/', imex_port.import_database, name='import_database'),
    path('administracion/export/mapa/', imex_port.export_mapa, name='export_mapa'),
    path('administracion/importar/mapa/', imex_port.import_mapa, name='import_mapa'),
]
