from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

<<<<<<< HEAD
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import openai
import os
=======
import os
import speech_recognition as sr
from django.conf import settings
>>>>>>> 949bd1f3e2e39d97f75742ff6bce922bbbbaa76d

from .forms import crearTarea
from . import models

<<<<<<< HEAD
openai.api_key = settings.OPENAI_API_KEY
=======

def recognize_speech_from_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Al parecer no se reconoce el Audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
>>>>>>> 949bd1f3e2e39d97f75742ff6bce922bbbbaa76d

# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        file_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        text = recognize_speech_from_audio(file_path)
        
        # Delete the temporary audio file after processing
        os.remove(file_path)
        
        return JsonResponse({'text': text})
    banners_all = models.Banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all,
        'active_page': 'inicio'
    })
    
@csrf_exempt
def ask(request):
    if request.method == 'POST':
        questionPOST = request.POST.get('question')

        # Buscar en la base de datos la información relevante
        faqs = models.Preguntas.objects.filter(pregunta__icontains=questionPOST)
        if faqs.exists():
            # Si se encuentra una pregunta en la base de datos, usar su respuesta
            answer = faqs.first().respuesta
        else:
            answer = None
        if not answer:
            # Si no se encuentra una respuesta en la base de datos, usar OpenAI para generar una respuesta
            context = "No relevant information found in the database."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Here is some context: {context} Now, answer this question: {questionPOST}"},
                ],
                max_tokens=150
            )
            total_tokens = response["usage"]["total_tokens"]
            try:
                answer = response['choices'][0]['message']['content'].strip()
            except KeyError:
                answer = "No se pudo obtener la respuesta del servidor."
        else:
            # Si se encontró una respuesta en la base de datos, usarla directamente
            pass
        return JsonResponse({'answer': answer, 'tokens':total_tokens})
    return JsonResponse({'error': 'Petición inválida'}, status=400)


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
@never_cache
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


# from django.db.models import Q
# import re
# import openai

# # Función para normalizar la entrada del usuario
# def normalize_input(input_string):
#     input_string = input_string.lower()
#     input_string = re.sub(r'[^\w\s]', '', input_string)
#     return input_string

# @csrf_exempt
# def ask(request):
#     if request.method == 'POST':
#         questionPOST = request.POST.get('question')
#         normalized_question = normalize_input(questionPOST)
        
#         # Tokenizar la pregunta normalizada
#         keywords = normalized_question.split()
        
#         # Crear una consulta que busque preguntas que contengan al menos una palabra clave
#         query = Q()
#         for keyword in keywords:
#             query |= Q(pregunta__icontains=keyword)
        
#         # Realizar la búsqueda en la base de datos
#         faqs = models.Preguntas.objects.filter(query)
#         if faqs.exists():
#             # Devolver la respuesta asociada a la primera pregunta encontrada en la base de datos
#             answer = faqs.first().respuesta
#         else:
#             # Si no se encuentra una respuesta en la base de datos, utilizar el modelo de OpenAI
#             response = openai.Completion.create(
#                 engine="text-davinci-003",  # Especificar el motor de OpenAI que deseas utilizar
#                 prompt=questionPOST,
#                 max_tokens=50  # Longitud máxima de la respuesta generada
#             )
#             answer = response.choices[0].text.strip()
#         return JsonResponse({'answer': answer})
#     return JsonResponse({'error': 'Petición inválida'}, status=400)
