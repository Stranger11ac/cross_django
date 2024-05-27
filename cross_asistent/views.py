from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.cache import never_cache

from .forms import crearTarea
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

@login_required
@never_cache
def singoutpage(request):
    logout(request)
    return redirect('singin')

@login_required
@never_cache
def dashbAdmin(request):
    errorMSG=''
    # tareas = models.Tareas.objects.all()
    tareas = models.Tareas.objects.filter(propietario = request.user)
    if request.method == 'POST':
        try:
            form_crearTarea = crearTarea(request.POST)
            nuevaTarea = form_crearTarea.save(commit=False)
            nuevaTarea.propietario = request.user
            nuevaTarea.save()
            return redirect('dashb_admin')
        
        except ValueError:
            errorMSG = 'Por favor introduzca datos Validos'
            
    return render(request, 'administracion/dashboard.html', {
        'form_crearTarea': crearTarea,
        'formError': errorMSG,
        'tareas_all': tareas,
        'active_page': 'inicio'
    })

@login_required
@never_cache
def tareaView(request, tarea_id):
    errorMSG=''
    tarea = get_object_or_404(models.Tareas, pk=tarea_id, propietario=request.user)
    if request.method == 'GET':
        tareaActualizar = crearTarea(instance=tarea)
    else:
        try:
            tareaActualizar = crearTarea(request.POST, instance=tarea)
            tareaActualizar.save()
            return redirect('dashb_admin')
        except ValueError:
            errorMSG = 'No se puede actualizar la tarea, Datos Invalidos'
    
    return render(request, 'administracion/tarea_view.html', {
        'tareaNum': tarea,
        'formEditar': tareaActualizar,
        'formError': errorMSG
    })