from django.urls import path
from . import views

urlpatterns = [
    # paginas de inicio
    path('', views.index, name='home'),
    path('chat/', views.chat_view, name='chatbot'),
    path('blog-eventos/', views.blog, name='blog'),
    path('mapa/', views.map, name='map'),
    path('acercade/', views.about, name='about'),
    path('preguntas-frecuentes/', views.faq, name='faq'),
    path('preguntas/', views.preguntas_view, name='preguntas'),
    path('consultaMap/', views.consultaMap, name='consultaMap'),
    path('obtenerEdificio/', views.obtenerEdificio, name='obtenerEdificio'),
    path('crearEditar/', views.crearEditar, name='crearEditar'),
    # Sesion y registro
    path('logout/', views.singoutpage, name='singout'),
    path('acceder/', views.singinpage, name='singin'),
    path('registro/', views.singuppage, name='singup'),
    # Administracion y programacion
    path('administracion/', views.vista_admin, name='vista_admin'),
    path('administracion/old/', views.dashbAdmin, name='dashb_admin'),
    path('administracion/programador/', views.vista_programador, name='vista_programador'),
    path('administracion/responderpreguntas/', views.responder_preguntas, name='responder_preguntas'),
    path('administracion/editaruser/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('administracion/activaruser/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('administracion/eliminaruser/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('administracion/desactivaruser/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('administracion/export/csv/', views.export_database, name='export_database_to_csv'),
    
    path('administracion/blogs/', views.admin_blogs, name='admin_blogs'),
    path('administracion/sendblog/', views.crear_articulo, name='send_blog'),
    path('administracion/sendimgsblog/', views.upload_image, name='send_imgsblog'),
    path('administracion/mapa/', views.mapa_form, name='admin_forms'),
    path('administracion/tarea/<int:tarea_id>/', views.tareaView, name='tareaView'),
]
