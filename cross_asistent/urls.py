from django.urls import path
from . import chatbot, functions, views, imex_port

urlpatterns = [
    # Páginas de inicio ----------------------------------------------------------
    path('', views.index, name='home'),
    path('preguntas_frecuentes/', views.fqt_questions, name='faq'),
    path('preguntar/', views.fqt_questions_send, name='enviar_preguntas'),
    path('blogs/', views.blogs, name='blog'),
    path('blogs/<int:Articulos_id>/', views.mostrar_blog, name='mostrar_blog'),
    path('calendario/', views.calendario, name='calendario'),
    path('calendario/eventos/', functions.calendario_eventos, name='calendario_eventos'),
    path('mapa/', views.map, name='map'),
    path('mapa/edificios/', functions.mapa_data, name='mapa_edificios'),
    path('acercade/', views.about, name='about'),
    
    # Chatbot y texto a voz ----------------------------------------------------------
    path('chatbot/', chatbot.chatbot, name='chatbot'),
    path('speekText/', chatbot.speekText, name='speekText'),
    path('start/', chatbot.start_recognition, name='start_recognition'),
    path('stop/', chatbot.stop_recognition, name='stop_recognition'),
    path('recognized_text/', chatbot.recognized_text, name='recognized_text'),
    
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
    path('administracion/usuarios/activacion/', functions.in_active, name='in_active'),
    path('administracion/usuarios/editar/<int:user_id>/', functions.editar_usuario, name='editar_usuario'),
    path('administracion/usuarios/eliminar/<int:user_id>/', functions.eliminar_usuario, name='eliminar_usuario'),
    
    # Banners ----------------------------------------------------------
    path('administracion/banners/', views.banners_page, name='upload_banner'),
    path('administracion/banners/editar/<int:banner_id>/', functions.banner_update, name='edit_banner'),
    path('administracion/banners/eliminar/<int:banner_id>/', functions.banner_delete, name='delete_banner'),
    path('administracion/banners/actualizar_visibilidad/', functions.banners_visibility_now, name='update_banner_visibility'),

    # Categorias ----------------------------------------------------------
    path('administracion/categorias/crear/', functions.categorias_create, name='categorias_create'),
    path('administracion/categorias/actualizar/', functions.categorias_update, name='categorias_update'),
    path('administracion/categorias/eliminar/', functions.categorias_delete, name='categorias_delete'),
    
    # Database ----------------------------------------------------------
    path('administracion/base_de_datos/', views.database_page, name='database_page'),
    path('administracion/database/crear/', functions.database_create, name='create_database'),
    path('administracion/database/actualizar/', functions.database_update, name='database_update'),
    path('administracion/database/eliminar/', functions.database_delete, name='database_delete'),
    path('administracion/calendario/', views.calendario_page, name='calendario_page'),
    path('administracion/preguntas/eliminar/', functions.preguntas_deleted, name='question_deleted'),

    # Blog ----------------------------------------------------------
    path('administracion/blog/crear/', views.blog_page, name='create_blog'),
    path('administracion/blog/editar/', functions.blog_change, name='blog_get'),
    path('administracion/blog/eliminar/', functions.blog_delete, name='blog_delete'),
    
    # Mapa ----------------------------------------------------------
    path('administracion/mapa/editar/', views.map_page, name='update_mapa'),
    path('administracion/mapa/modificar/', views.update_create_pleace_map, name='upload_map'),
    path('administracion/mapa/eliminar/', functions.delete_pleaceMap, name='del_pleace_map'),
    path('administracion/mapa/elimiina/database/', functions.delete_pleaceMap_DB, name='del_pleace_mapdb'),
    
    # Galeria ----------------------------------------------------------
    path('administracion/galeria/subir/', views.upload_image, name='send_imgsblog'),
    path('administracion/galeria/lista/', views.lista_imagenes, name='lista_imagenes'),
    
    # Notificaciones ----------------------------------------------------------
    path('administracion/notificaciones/', views.ver_notis, name='notificaciones'),
    path('administracion/notificaciones/notificacion_leida/', views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),
    
    # Importar y Exportar ----------------------------------------------------------
    path('administracion/export/categorias/', imex_port.export_categorias, name='export_categorias'),
    path('administracion/importar/categorias/', imex_port.import_categorias, name='import_categorias'),
    path('administracion/export/database/', imex_port.export_database, name='export_database'),
    path('administracion/importar/database/', imex_port.import_database, name='import_database'),
    path('administracion/export/mapa/', imex_port.export_mapa, name='export_mapa'),
    path('administracion/importar/mapa/', imex_port.import_mapa, name='import_mapa'),
]