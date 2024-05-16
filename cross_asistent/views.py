from django.shortcuts import render
from . import models
from django.http import HttpResponse

# Create your views here.
def index(request):
    banners_all = models.banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all
    })

def faq(request):
    proyectosall = models.proyectos.objects.all()
    return render(request, 'frecuentes.html', {
        'proyectos_all': proyectosall
    })
