from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('frecuentes/', views.faq),
    path('blog/', views.faq),
    path('mapa/', views.faq),
]
