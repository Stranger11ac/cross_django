from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

from .forms import crearTarea
from . import models

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def index(request):
    banners_all = models.Banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all,
        'active_page': 'inicio'
    })

def process_question(question):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('spanish'))
    tokens = word_tokenize(question)
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    print(tokens)
    return tokens

def contains_keyword(tokens, keyword):
    return keyword in tokens

def find_answer(question):
    tokens = process_question(question)
    
    synonyms = models.Synonym.objects.filter(synonym__in=tokens)
    synonym_dict = {synonym.synonym: synonym.keyword for synonym in synonyms}
    keywords = [synonym_dict[token] for token in tokens if token in synonym_dict]
    
    if keywords:
        pregunta_model = models.Database.objects.filter(titulo__in=keywords).first()
        if pregunta_model:
            return pregunta_model.informacion
    
    all_preguntas = models.Database.objects.all()
    preguntas_tokens = [(pregunta, set(process_question(pregunta.titulo))) for pregunta in all_preguntas]
    
    best_match = None
    best_match_score = 0
    
    for pregunta, pregunta_tokens in preguntas_tokens:
        match_count = len(set(tokens).intersection(pregunta_tokens))
        if match_count > best_match_score:
            best_match = pregunta
            best_match_score = match_count
    
    if best_match:
        return f'{best_match.informacion}<br> ¿Puedo ayudarte en algo más?'

    return "Lo siento, no encontré información sobre tu pregunta."

def chat_view(request):
    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            answer = find_answer(question)
            return JsonResponse({'success': True, 'answer': answer})
        return JsonResponse({'success': False, 'message': 'No se proporcionó ninguna pregunta.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def faq(request):
    questall = models.Database.objects.filter(frecuencia__gt=0).order_by('-frecuencia')
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
    edificios = [
        {
            'nombre': 'Edificio 4',
            'descripcion': 'Descripción del Edificio 4',
            'imagen_url': 'img/qr_phtone.png',
            'coordenadas': [[25.55661, -100.93688], [25.55633, -100.93647], [25.55613, -100.93662], [25.55642, -100.93703]]
        },
        {
            'nombre': 'Centro de Idiomas',
            'descripcion': 'Descripción del Centro de Idiomas',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55715, -100.93684], [25.55742, -100.93724], [25.55757, -100.93711], [25.55731, -100.93670]]
        },
        {
            'nombre': 'Laboratorio 7B',
            'descripcion': 'Descripción del Laboratorio 7B',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55704, -100.93644], [25.55718, -100.93631], [25.55694, -100.93593], [25.55679, -100.93606]]
        },
        {
            'nombre': 'Vinculación',
            'descripcion': 'Descripción de Vinculación',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55813, -100.93653], [25.55794, -100.93623], [25.55765, -100.93646], [25.55785, -100.93676]]
        },
         {
            'nombre': 'Rectoria',
            'descripcion': 'Descripcion de Rectoria',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55767,-100.93590], [25.55748,-100.93559],[25.55719,-100.93581],[25.55741,-100.93612]]
        },
         {
            'nombre': 'Biblioteca',
            'descripcion': 'Descripción de Bibliotecaaaaaaaaaaaaaaaa',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [ [25.55651,-100.93613], [25.55639,-100.93594], [25.55615,-100.93616], [25.55628,-100.93633]]
        },
         {
            'nombre': 'Cafeteria UTC',
            'descripcion': 'Descripción de Cafeteria UTC',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [ [25.55616,-100.93610],[25.55607,-100.93618],[25.55599,-100.93608],[25.55607,-100.93601]]
        },
         {
            'nombre': 'Edificio 3',
            'descripcion': 'Descripción de Edificio 3',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55611,-100.93582],[25.55583,-100.93547],[25.55566,-100.93564],[25.55594,-100.93600],]
        },
         {
            'nombre': 'Domo',
            'descripcion': 'Descripción de Domo',
            'imagen_url': 'img/Domo.webp',
            'coordenadas': [[25.55552,-100.93498],[25.55533,-100.93471],[25.55515,-100.93486],[25.55534,-100.93514],]
        },
          {
            'nombre': 'Edificio 2',
            'descripcion': 'Descripción del Edificio 2',
            'imagen_url': 'img/Edificio2.webp',
            'coordenadas': [[25.55495, -100.93495], [25.55471, -100.93458], [25.55455, -100.93471], [25.55479, -100.93508]]
        },
        {
            'nombre': 'Laboratorio 5',
            'descripcion': 'Descripción del Laboratorio 5',
            'imagen_url': 'img/Laboratorio 4-E.webp',
            'coordenadas': [[25.55527, -100.93468], [25.55515, -100.93479], [25.55503, -100.93462], [25.55515, -100.93451]]
        },
        {
            'nombre': 'Cafeteria UTC 1',
            'descripcion': 'Descripción de Cafeteria UTC 1',
            'imagen_url': 'img/cafeteria1.webp',
            'coordenadas': [[25.55501, -100.93408], [25.55482, -100.93430], [25.55473, -100.93421], [25.55491, -100.93399]]
        },
         {
            'nombre': 'Edificio 1',
            'descripcion': 'Descripción del Edificio 1',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55527, -100.93369], [25.55545, -100.93352], [25.55575, -100.93393], [25.55556, -100.93409]]
        },
        {
            'nombre': 'Laboratorio de PLC',
            'descripcion': 'Descripción del Laboratorio de PLC',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55573, -100.93424], [25.55586, -100.93411], [25.55615, -100.93447], [25.55602, -100.93461]]
        },
        {
            'nombre': 'Caceta 1',
            'descripcion': 'Descripción de Caceta 1',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55821,-100.93682], [25.55815,-100.93672], [25.55805,-100.93682], [25.55812,-100.93691]]
        },
        {
            'nombre': 'Caceta 2',
            'descripcion': 'Descripción de Caceta 2',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55606,-100.93464], [25.55613,-100.93457], [25.55624,-100.93470], [25.55616,-100.93477]]
        },
        {
            'nombre': 'Oxxo',
            'descripcion': 'Descripción de Oxxo',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55777,-100.93619], [25.55785,-100.93613], [25.55776,-100.93602], [25.55769,-100.93610]]
        },
        {
            'nombre': 'Papeleria',
            'descripcion': 'Descripción de Papeleria',
            'imagen_url': 'img/qr_2.png',
            'coordenadas': [[25.55700,-100.93713], [25.55708,-100.93709], [25.55704,-100.93701], [25.55697,-100.93706]]
        },
    ]
    return render(request, 'mapa.html', {
        'edificios': edificios,
        'active_page': 'map'
    })

def about(request):
    return render(request, 'about.html', {
        'active_page': 'about'
    })

# Administracion ----------------------------------------------------------
@never_cache
def singuppage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password1 and password2 and username:
            if password1 == password2:
                try:
                    newUser = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, is_active=0)
                    newUser.save()
                    return JsonResponse({'success': True, 'message': 'Usuario creado 🥳<br> Tu cuenta esta <u>INACTIVA</u>'}, status=200)
                except IntegrityError:
                    return JsonResponse({'success': False, 'message': f'El usuario <u>{username}</u> ya existe 😯'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Las contraseñas no coinciden 😬'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Datos incompletos 😅'}, status=400)
    else:
        logout(request)
        return render(request, 'administracion/singup.html')

@never_cache
def singinpage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        usernamePOST = request.POST.get('username')
        passwordPOST = request.POST.get('password')
        
        user = authenticate(request, username=usernamePOST, password=passwordPOST)
        if user is None:
            return JsonResponse({'success': False, 'message': 'Revisa el usuario o contraseña 😅. Verifica que tu cuenta esté habilitada'}, status=400)
        else:
            login(request, user)
            if user.is_staff:
                return JsonResponse({'success': False, 'prog_admin': True}, status=200)
            if (request, user.is_staff):
                return JsonResponse({'success': 'prog'}, status=200)
            return JsonResponse({'success': True}, status=200)
    else:
        logout(request)
        return render(request, 'administracion/singin.html', {
            'active_page': 'singin'
        })

@login_required
@never_cache
def singoutpage(request):
    logout(request)
    return redirect('singin')

@login_required
@never_cache
def dashbAdmin(request):
    errorMSG = ''
    tareas = models.Tareas.objects.filter(propietario=request.user)
    if request.method == 'POST':
        try:
            form_crearTarea = crearTarea(request.POST)
            nuevaTarea = form_crearTarea.save(commit=False)
            nuevaTarea.propietario = request.user
            nuevaTarea.save()
            return redirect('dashb_admin')
        except ValueError:
            errorMSG = 'Por favor introduzca datos válidos'
            
    return render(request, 'administracion/dashboard.html', {
        'form_crearTarea': crearTarea,
        'formError': errorMSG,
        'tareas_all': tareas,
        'active_page': 'inicio'
    })

@login_required
@never_cache
def tareaView(request, tarea_id):
    errorMSG = ''
    tarea = get_object_or_404(models.Tareas, pk=tarea_id, propietario=request.user)
    if request.method == 'GET':
        tareaActualizar = crearTarea(instance=tarea)
    else:
        try:
            tareaActualizar = crearTarea(request.POST, instance=tarea)
            tareaActualizar.save()
            return redirect('dashb_admin')
        except ValueError:
            errorMSG = 'No se puede actualizar la tarea, datos inválidos'
    
    return render(request, 'administracion/tarea_view.html', {
        'tareaNum': tarea,
        'formEditar': tareaActualizar,
        'formError': errorMSG
    })

# def para la vista administrador
@login_required
@never_cache
def vista_admin(request):
    blogs_all = models.Articulos.objects.filter()
    user = request.user
    
    context = {
        'user': user,
        'num_blogs': blogs_all.count(),  
        'blogs_all': blogs_all, 
    }

    return render(request, 'administracion/vista_admin.html', context)

@login_required
@never_cache
def vista_programador(request):
    num_blogs = models.Articulos.objects.filter().count()
    num_preguntas = models.Database.objects.filter().count()
    user = request.user
    users = User.objects.filter()
    blogs_all = models.Articulos.objects.filter()
    
    return render(request, 'administracion/vista_programador.html', {
        'num_blogs': num_blogs,
        'num_preguntas': num_preguntas,
        'user': user,  
        'blogs_all': blogs_all,
        'users': users,
    })

# def para responder preguntas
@login_required
@never_cache
def responder_preguntas(request):
    if request.method == 'POST':
        pregunta_id = request.POST.get('pregunta_id')
        respuesta = request.POST.get('respuesta')
        pregunta = models.Database.objects.get(id=pregunta_id)
        pregunta.respuesta = respuesta
        pregunta.save()
        return redirect('vista_programador')
    
    return redirect('vista_programador')

@login_required
@never_cache
def activar_usuario(request, user_id):
    if request.user.is_staff:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
    return redirect('vista_programador')
