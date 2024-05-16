from django.shortcuts import render
from . import models
from django.http import HttpResponse

# Create your views here.
def index(request):
    banners_all = models.banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all
    })
    # return HttpResponse("<h1>Inicio Cross Project</h1>")

def faq(request):
    proyectosall = models.proyectos.objects.all()
    return render(request, 'faq.html', {
        'proyectos_all': proyectosall
    })
    # return HttpResponse("<h1>Inicio Preguntas frecuentes</h1>")
