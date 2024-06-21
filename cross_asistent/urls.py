from django.urls import path
from . import views

urlpatterns = [
    # Páginas de inicio
    path('', views.index, name='home'),
    path('chat/', views.chat_view, name='chatbot'),
    path('blog-eventos/', views.blog, name='blog'),
    path('mapa/', views.map, name='map'),  # Ruta para la página del mapa
    path('acercade/', views.about, name='about'),
    path('preguntas-frecuentes/', views.faq, name='faq'),
    path('preguntas/', views.preguntas_view, name='preguntas'),

    # Sesión y registro
    path('logout/', views.singoutpage, name='singout'),
    path('administracion/acceder/', views.singinpage, name='singin'),
    path('administracion/registro/', views.singuppage, name='singup'),

    # Administración y programación
    path('administracion/', views.vista_admin, name='vista_admin'),
    path('administracion/old/', views.dashbAdmin, name='dashb_admin'),
    path('administracion/programador/', views.vista_programador, name='vista_programador'),
    path('administracion/responder_preguntas/', views.responder_preguntas, name='responder_preguntas'),
    path('administracion/editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('administracion/activar_usuario/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('administracion/eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('administracion/desactivar_usuario/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('administracion/export/csv/', views.export_database, name='export_database_to_csv'),
<<<<<<< HEAD

    path('administracion/formularios/', views.forms_admin, name='forms'),
=======
    
    path('administracion/blogs/', views.admin_blogs, name='admin_blogs'),
    path('administracion/send_blog/', views.crear_articulo, name='send_blog'),
    path('administracion/mapa/', views.mapa_form, name='admin_forms'),
>>>>>>> d3a91a2c4f193b97d02f2ee408369f75243aa032
    path('administracion/tarea/<int:tarea_id>/', views.tareaView, name='tareaView'),

    # Nueva ruta para mapa2
    path('mapa2/', views.mapa2, name='mapa2'),
]
