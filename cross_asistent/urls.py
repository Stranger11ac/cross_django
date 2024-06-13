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
    path('administracion/', views.dashbAdmin, name='dashb_admin'),
    path('administracion/tarea/<int:tarea_id>/', views.tareaView, name='tareaView'),
    path('chat/', views.chat_view, name='chatbot'),
# se agrego la url para la vista administrador
    path('administracion/vista_admin/', views.vista_admin, name='vista_admin'),
    path('administracion/vista_programador/', views.vista_programador, name='vista_programador'),
    # path de responder preguntas
    path('responder_preguntas/', views.responder_preguntas, name='responder_preguntas'),
#path para exportar a csv
    path('export/csv/', views.export_database_to_csv, name='export_database_to_csv'),
# path para activar los usuarios
    path('activar_usuario/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('desactivar_usuario/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('logout/', views.singoutpage, name='singout'),
]
