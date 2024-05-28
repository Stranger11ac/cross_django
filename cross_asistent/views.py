from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
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

def about(request):
    return render(request, 'about.html', {
        'active_page': 'about'
    })

# Administracion --------------------------------------------
def singuppage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        
        if password1 and password2 and username:
            if password1 == password2:
                try:
                    newUser = User.objects.create_user(username=username, password=password1, is_active=0)
                    newUser.save()
                    login(request, newUser)
                    return JsonResponse({'success': True, 'message': 'Usuario creado 🥳<br> Tu cuenta esta <u>INACTIVA</u>'}, status=200)
                except IntegrityError:
                    return JsonResponse({'success': False, 'message': f'El usuario <u>{username}</u> ya existe 😯'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Las contraseñas no coinciden 😬'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Datos incompletos 😅'}, status=400)
    else:
        return render(request, 'administracion/singup.html', {
            'form': UserCreationForm()
        })


def singinpage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        usernamePOST = request.POST.get('username')
        passwordPOST = request.POST.get('password')
        
        user = authenticate(request, username=usernamePOST, password=passwordPOST)
        if user is None:
            return JsonResponse({'success': False, 'message': 'Revisa el usuario o contraseña 😅. Verifica que tu cuenta esté habilitada'}, status=400)
        else:
            login(request, user)
            return JsonResponse({'success': True}, status=200)
    else:
        return render(request, 'administracion/singin.html', {
            'active_page': 'singin',
            'form': AuthenticationForm()
        })

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