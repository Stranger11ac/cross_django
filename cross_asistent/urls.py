from django.urls import path
from . import views, elements

urlpatterns = [
    # Páginas de inicio
    path('', views.index, name='home'),
    path('chatbot/', elements.chatbot, name='chatbot'),
    path('blog-eventos/', views.blog, name='blog'),
    path('blog/<int:Articulos_id>/', views.mostrar_blog, name='mostrar_blog'),
    path('mapa/', views.map, name='map'),
    path('acercade/', views.about, name='about'),
    path('preguntas_frecuentes/', views.faq, name='faq'),
    path('preguntar/', views.crear_pregunta, name='preguntas'),
    
    # Sesion y registro
    path('logout/', views.singoutpage, name='singout'),
    path('password-reset/', views.password_reset_request, name='password_reset_email'),
    path('acceder/', views.singinpage, name='singin'),
    path('registro/', views.singuppage, name='singup'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Administracion y programacion
    path('administracion/', views.vista_admin, name='vista_admin'),
    path('administracion/programador/', views.vista_programador, name='vista_programador'),
    path('administracion/perfil/', views.ver_perfil, name='perfil'),
    path('administracion/responderpreguntas/', views.responder_preguntas, name='responder_preguntas'),
    path('administracion/export/csv/', views.export_database, name='export_database_to_csv'),
    path('administracion/importar/csv/', views.import_database, name='import_database'),
    path('banners/', views.upload_banner, name='upload_banner'),
    path('administracion/banners/<int:banner_id>/edit/', views.edit_banner, name='edit_banner'),
    path('banners/delete/<int:banner_id>/', views.delete_banner, name='delete_banner'),
    
    # usuarios
    path('administracion/modificar_usuario/', views.in_active, name='in_active'),
    path('administracion/editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('administracion/eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # Blog
    path('administracion/blogs/', views.admin_blogs, name='admin_blogs'),
    path('administracion/crear_blog/', views.crear_articulo, name='send_blog'),
    path('administracion/registrar_img_blog/', views.upload_image, name='send_imgsblog'),
    path('administracion/lista_imagenes/', views.lista_imagenes, name='lista_imagenes'),
    
    # Mapa
    path('administracion/obtener_edificio/', views.obtenerEdificio, name='obtenerEdificio'),
    path('administracion/editar_mapa/', views.obtenerinfoEdif, name='consultaMap'),
    path('administracion/crearEditar_mapa/', views.crearEditarMapa, name='crearEditar'),
]
