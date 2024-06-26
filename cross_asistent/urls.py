from django.urls import path
from . import views

urlpatterns = [
    # Páginas de inicio
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('blog-eventos/', views.blog, name='blog'),
    path('blog/<int:Articulos_id>/', views.mostrar_blog, name='mostrar_blog'),
    path('mapa/', views.map, name='map'),
    path('acercade/', views.about, name='about'),
    path('preguntas_frecuentes/', views.faq, name='faq'),
    path('preguntar/', views.crear_pregunta, name='preguntas'),
    
    # Sesion y registro
    path('logout/', views.singoutpage, name='singout'),
    path('acceder/', views.singinpage, name='singin'),
    path('registro/', views.singuppage, name='singup'),
    
    # Administracion y programacion
    path('administracion/', views.vista_admin, name='vista_admin'),
    path('administracion/programador/', views.vista_programador, name='vista_programador'),
    path('administracion/responderpreguntas/', views.responder_preguntas, name='responder_preguntas'),
    # path('administracion/export_table_to_csv/', views.export_table_to_csv, name='export_table_to_csv'),
    # path('administracion/consulTabla/', views.consulTabla, name='consulTabla'),
    path('administracion/banners/', views.upload_banner, name='banners'),
    
    # usuarios
    path('administracion/editaruser/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('administracion/activaruser/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('administracion/eliminaruser/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('administracion/desactivaruser/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    
    # blog
    path('administracion/blogs/', views.admin_blogs, name='admin_blogs'),
    path('administracion/crear_blog/', views.crear_articulo, name='send_blog'),
    path('administracion/registrar_img_blog/', views.upload_image, name='send_imgsblog'),
    
    # mapa
    path('administracion/obtener_edificio/', views.obtenerEdificio, name='obtenerEdificio'),
    path('administracion/editar_mapa/', views.obtenerinfoEdif, name='consultaMap'),
    path('administracion/crearEditar_mapa/', views.crearEditarMapa, name='crearEditar'),

    # Nueva ruta para mapa2
    path('mapa2/', views.mapa2, name='mapa2'),
]
