from django.shortcuts import render
from . import models
from django.http import HttpResponse

# Create your views here.
def index(request):
    banners_all = models.banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all,
        'active_page': 'inicio'
    })

def faq(request):
    questall = models.preguntas.objects.all()
    return render(request, 'frecuentes.html', {
        'quest_all': questall,
        'active_page': 'faq'
    })
    
def blog(request):
    blogs = models.articulos.objects.all()
    return render(request, 'blog.html', {
        'blogs_all': blogs,
        'active_page': 'blog'
    })

def map(request):
    return render(request,'mapa.html', {
        'active_page': 'map'
    })

def formsAdmin(request):
    return render(request, 'administracion/layout.html')