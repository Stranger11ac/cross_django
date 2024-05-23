from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate ,logout
from django.db import IntegrityError

from . import models

# Create your views here.
def index(request):
    banners_all = models.Banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all,
        'active_page': 'inicio'
    })

def faq(request):
    questall = models.Preguntas.objects.all()
    return render(request, 'frecuentes.html', {
        'quest_all': questall,
        'active_page': 'faq'
    })

def blog(request):
    blogs = models.Articulos.objects.all()
    return render(request, 'blog.html', {
        'blogs_all': blogs,
        'active_page': 'blog'
    })

def map(request):
    return render(request,'mapa.html', {
        'active_page': 'map'
    })

# Administracion --------------------------------------------
def singuppage(request):
    errorMSG = ''
    if request.method == 'GET':
        return render(request, 'administracion/singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                newUser = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                newUser.save()
                login(request, newUser)
                return redirect('singin')
            except IntegrityError:
                errorMSG = 'El usuario ya existe'
        else:
            errorMSG = 'Las contraseñas no coinciden'
            
    return render(request, 'administracion/singup.html', {
        'form': UserCreationForm,
        'formError': errorMSG
    })
    

def singinpage(request):
    if request.method == 'GET':
        return render(request, 'administracion/singin.html', {
            'active_page': 'singin',
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            errorMSG = 'El usuario o contraseña son incorrectos'
            return render(request, 'administracion/singin.html', {
                'active_page': 'singin',
                'form': AuthenticationForm,
                'formError': errorMSG
            })
        else:
            login(request, user)
            return redirect('dashb_admin')
            

def singoutpage(request):
    logout(request)
    return redirect('singin')

def dashbAdmin(request):
    return render(request, 'administracion/dashboard.html')