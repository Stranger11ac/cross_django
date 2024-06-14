from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('preguntas-frecuentes/', views.faq, name='faq'),
    path('blog-eventos/', views.blog, name='blog'),
    path('mapa/', views.map, name='map'),
    path('acercade/', views.about, name='about'),
    path('administracion/acceder/', views.singinpage, name='singin'),
    path('administracion/registro/', views.singuppage, name='singup'),
    path('administracion/old/', views.dashbAdmin, name='dashb_admin'),
    path('administracion/tarea/<int:tarea_id>/', views.tareaView, name='tareaView'),
    path('chat/', views.chat_view, name='chatbot'),
# se agrego la url para la vista administrador
    path('administracion/', views.vista_admin, name='vista_admin'),
    path('administracion/programador/', views.vista_programador, name='vista_programador'),
# path de responder preguntas
    path('administracion/responder_preguntas/', views.responder_preguntas, name='responder_preguntas'),
#path para exportar a csv
    path('administracion/export/csv/', views.export_database_to_csv, name='export_database_to_csv'),
# path para activar los usuarios
    path('administracion/activar_usuario/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('administracion/desactivar_usuario/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('administracion/eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('administracion/editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('administracion/formularios/', views.forms_admin, name='forms'),
    
    path('logout/', views.singoutpage, name='singout'),
]
