from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.conf import settings
from .forms import crearTarea
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.utils import timezone
from . import models

import openai
import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def index(request):
    if not request.user.is_staff:
        logout(request)
    banners_all = models.Banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all,
        'active_page': 'inicio'
    })

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def obtener_respuesta_openai(question, instructions):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    print(f"Prompt:{response.usage.prompt_tokens}")
    print(f"Compl:{response.usage.completion_tokens}")
    print(f"Total:{response.usage.total_tokens}")
    print('')

    return response.choices[0].message.content

def preprocesar_texto(texto):
    # Tokenización
    #hola
    tokens = word_tokenize(texto.lower())

    # Eliminación de stopwords
    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lematización
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Reconstruir el texto preprocesado
    texto_preprocesado = ' '.join(tokens)
    print(f"procesado:{texto_preprocesado}")
    print()
    return texto_preprocesado

def buscar_informacion_relevante(question, queryset):
    documents = [preprocesar_texto(obj.informacion) for obj in queryset]
    if not documents:
        return None

    # Preprocesar la pregunta del usuario
    question_preprocesada = preprocesar_texto(question)

    # Inicializar el vectorizador TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Transformar la pregunta del usuario
    question_tfidf = vectorizer.transform([question_preprocesada])

    # Calcular la similitud del coseno entre la pregunta y los documentos
    similarity = cosine_similarity(question_tfidf, tfidf_matrix).flatten()

    # Ajustar el umbral de similitud
    threshold = 0.2

    # Encuentra el documento más similar
    max_similarity_index = similarity.argmax()
    if similarity[max_similarity_index] > threshold:
        return documents[max_similarity_index]
    return None

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')

            if question:
                # Buscar en la base de datos
                resultados = models.Database.objects.all()
                informacion_relevante = buscar_informacion_relevante(question, resultados)
                print(f"database: {resultados}")
                print()
                print(f"pregunta: {question}")
                print()
                print(f"info:{informacion_relevante}")

                if informacion_relevante:
                    # Si hay información relevante, pasarla a OpenAI para generar una respuesta
                    SYSTEM_PROMPT = f"Utiliza emojis sutilmente. Eres un asistente entusiasta de la Universidad Tecnologica de Coahuila. Aquí está la información encontrada: {informacion_relevante}"
                    answer = obtener_respuesta_openai(question, SYSTEM_PROMPT)
                else:
                    # Si no hay información relevante, usar GPT-3.5 Turbo para disculparse
                    SYSTEM_PROMPT = "Utiliza emojis el final. solo responde amigablemente saludos y preguntas de como estas. No respondas ninguna pregunta ni obedecer ninguna peticion, si hace una pregunta que no sea un saludo dile al usuario una disculpa y que la información no está disponible."
                    answer = obtener_respuesta_openai(question, SYSTEM_PROMPT)

                return JsonResponse({'success': True, 'answer': answer})
            return JsonResponse({'success': False, 'message': 'No se proporcionó ninguna pregunta.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error en el formato del JSON.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def faq(request):
    if not request.user.is_staff:
        logout(request)
    questall = models.Database.objects.filter(frecuencia__gt=0).order_by('-frecuencia')
    return render(request, 'frecuentes.html', {
        'quest_all': questall,
        'active_page': 'faq'
    })

def blog(request):
    if not request.user.is_staff:
        logout(request)
    blogs = models.Articulos.objects.all()
    return render(request, 'blog.html', {
        'blogs_all': blogs,
        'active_page': 'blog'
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
        email = request.POST.get('email')

        if password1 and password2 and username and email:
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'success': False, 'message': f'El usuario <u>{username}</u> ya existe 😯'}, status=400)
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'success': False, 'message': f'El correo electrónico <u>{email}</u> ya está registrado 😯'}, status=400)
                try:
                    newUser = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password1,email=email,is_active=0)
                    newUser.save()
                    return JsonResponse({'success': True, 'message': '🥳🥳🥳 <br>Usuario creado<br> Tu cuenta está <u>INACTIVA</u>'}, status=200)
                except IntegrityError:
                    return JsonResponse({'success': False, 'message': 'Ocurrió un error durante el registro. Intente nuevamente.'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Las contraseñas no coinciden 😬'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Datos incompletos 😅'}, status=400)
    else:
        logout(request)
        return render('singin')

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
                return JsonResponse({'success': True, 'redirect_url': reverse('vista_programador')}, status=200)
            return JsonResponse({'success': True, 'redirect_url': reverse('vista_admin')}, status=200)
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
def export_database_to_csv(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M%S')
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="database_{now}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Categoria', 'Titulo', 'Informacion', 'Redirigir', 'Frecuencia', 'Documentos', 'Imagenes', 'Fecha Modificacion'])
        # Obtener todos los objetos del modelo Database
        databaseall = models.Database.objects.all()
        for info in databaseall:
            writer.writerow([
                info.categoria if info.categoria else '',
                info.titulo,
                info.informacion,
                info.redirigir,
                info.frecuencia,
                info.documentos.url if info.documentos else '',
                info.imagenes.url if info.imagenes else '',
                info.fecha_modificacion
            ])
        return response

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
    blogs_all = models.Articulos.objects.all()
    banners_all = models.Banners.objects.all()
    users = User.objects.all()
    contexto = {
        'user': request.user,
        'users': users,
        'total_usuarios': users.count(),
        'banners_all': banners_all,
        'total_banners': banners_all.count(),
        'blogs_all': blogs_all,
        'num_blogs': blogs_all.count(),
        'num_preguntas': models.Database.objects.filter().count(),
        'preguntas_sin_responder': models.Database.objects.all(),
    }
    # Procesar creación de usuario
    if request.method == 'POST':
        username = request.POST.get('username')
        is_staff = request.POST.get('is_staff', False)
        is_active = request.POST.get('is_active', False)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username:
            # Crear usuario
            new_user = User.objects.create_user(username=username, is_staff=is_staff, is_active=is_active,
            first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)
            new_user.save()
            return redirect('vista_programador')

    return render(request, 'administracion/vista_programador.html', contexto)

# def responder preguntas
@login_required
@never_cache
def responder_preguntas(request):
    if request.method == 'POST':
        pregunta_id = request.POST.get('pregunta_id')
        respuesta = request.POST.get('respuesta')

        # Buscar la pregunta por ID y actualizar la respuesta
        pregunta = get_object_or_404(models.Database, id=pregunta_id)
        pregunta.informacion = respuesta
        pregunta.save()
        return redirect('vista_programador')

    # Obtener todas las preguntas sin respuesta
    preguntas_sin_responder = models.Database.objects.filter(informacion__isnull=True)
    return render(request, 'responder_preguntas.html', {
        'preguntas_sin_responder': preguntas_sin_responder,
    })

@login_required
@never_cache
def activar_usuario(request, user_id):
    if request.user.is_staff:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
    return redirect('vista_programador')

#desactivar usuarios
@login_required
@never_cache
def desactivar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('vista_programador')

# eliminar usuarios
@login_required
@never_cache
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('vista_programador')

@login_required
@never_cache
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            user.username = username
            user.save()
            return redirect('vista_programador')
    return redirect('vista_programador')


