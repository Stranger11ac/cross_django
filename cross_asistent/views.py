from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.conf import settings
from .forms import crearTarea
from django.http import HttpResponse
from .models import Database
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
    logout(request)
    questall = models.Database.objects.filter(frecuencia__gt=0).order_by('-frecuencia')
    return render(request, 'frecuentes.html', {
        'quest_all': questall,
        'active_page': 'faq'
    })

def blog(request):
    logout(request)
    blogs = models.Articulos.objects.all()
    return render(request, 'blog.html', {
        'blogs_all': blogs,
        'active_page': 'blog'
    })

def map(request):
    logout(request)
    edificios = [
        {
            'edifcolor': 'red','edifill': 'red',
            'nombre': 'Edificio 4',
            'descripcion': 'Descripción del Edificio 4',
            'imagen_url': 'img/Edificio_4.webp',
            'coordenadas': [[25.55661, -100.93688], [25.55633, -100.93647], [25.55613, -100.93662], [25.55642, -100.93703]],
            'centro': [25.55637, -100.93675]
        },
        {
            'edifcolor': 'orange','edifill': 'orange',
            'nombre': 'Centro de Idiomas',
            'descripcion': 'Descripción del Centro de Idiomas',
            'imagen_url': 'img/Centro_Idiomas.webp',
            'coordenadas': [[25.55715, -100.93684], [25.55742, -100.93724], [25.55757, -100.93711], [25.55731, -100.93670]],
            'centro': [25.55735, -100.93697]
        },
        {
            'edifcolor': '#00FFFF','edifill': '#00FFFF',
            'nombre': 'Laboratorio 7B',
            'descripcion': 'Descripción del Laboratorio 7B',
            'imagen_url': 'img/Laboratorio_7B.webp',
            'coordenadas': [[25.55704, -100.93644], [25.55718, -100.93631], [25.55694, -100.93593], [25.55679, -100.93606]],
            'centro': [25.55700, -100.93620]
        },
        {
            'edifcolor': 'yellow','edifill': 'yellow',
            'nombre': 'Vinculación',
            'descripcion': 'Descripción de Vinculación',
            'imagen_url': 'img/Vinculacion.webp',
            'coordenadas': [[25.55813, -100.93653], [25.55794, -100.93623], [25.55765, -100.93646], [25.55785, -100.93676]],
            'centro': [25.55790, -100.93650]
        },
        {
            'edifcolor': 'yellow','edifill': 'yellow',
            'nombre': 'Rectoria',
            'descripcion': 'Descripcion de Rectoria',
            'imagen_url': 'img/Rectoria.webp',
            'coordenadas': [[25.55767, -100.93590], [25.55748, -100.93559], [25.55719, -100.93581], [25.55741, -100.93612]],
            'centro': [25.55742, -100.93587]
        },
        {
            'edifcolor': 'blue','edifill': 'blue',
            'nombre': 'Biblioteca',
            'descripcion': 'Descripción de Biblioteca',
            'imagen_url': 'img/Biblioteca.webp',
            'coordenadas': [[25.55651, -100.93613], [25.55639, -100.93594], [25.55615, -100.93616], [25.55628, -100.93633]],
            'centro': [25.55632, -100.93615]       
        },
        {
            'edifcolor': 'green','edifill': 'green',
            'nombre': 'Cafeteria UTC',
            'descripcion': 'Descripción de Cafeteria UTC',
            'imagen_url': 'img/Cafeteria_UTC.webp',
            'coordenadas': [[25.55616, -100.93610], [25.55607, -100.93618], [25.55599, -100.93608], [25.55607, -100.93601]],
            'centro': [25.55608, -100.93611]
        },
        {
            'edifcolor': 'red','edifill': 'red',
            'nombre': 'Edificio 3',
            'descripcion': 'Descripción de Edificio 3',
            'imagen_url': 'img/Edificio_3.webp',
            'coordenadas': [[25.55611, -100.93582], [25.55583, -100.93547], [25.55566, -100.93564], [25.55594, -100.93600]],
            'centro': [25.55589, -100.93575]
        },
        {
            'edifcolor': 'white','edifill': 'white',
            'nombre': 'Domo',
            'descripcion': 'Descripción de Domo',
            'imagen_url': 'img/Domo.webp',
            'coordenadas': [[25.55552, -100.93498], [25.55533, -100.93471], [25.55515, -100.93486], [25.55534, -100.93514]],
            'centro': [25.55533, -100.93493]
        },
        {
            'edifcolor': 'red','edifill': 'red',
            'nombre': 'Edificio Docente 2',
            'titulo': 'Tecnologias de la Informacion y Comunicacion',
            'descripcion': '<h5>Carreras:</h5> <ul>Desarrollo y Gestion de Software Multiplataforma<br>Entornos Virtuales y Negocios Digitales<br>Diseño y Gestion de Redes Logisticas</ul> ',
            'imagen_url': 'img/Edificio_2.webp',
            'coordenadas': [[25.55495, -100.93495], [25.55471, -100.93458], [25.55455, -100.93471], [25.55479, -100.93508]],
            'centro': [25.55474, -100.93482]
        },
        {
            'edifcolor': '#00FFFF','edifill': '#00FFFF',
            'nombre': 'Laboratorio 4-E',
            'descripcion': 'Descripción del Laboratorio 4-E',
            'imagen_url': 'img/Laboratorio_4-E.webp',
            'coordenadas': [[25.55527, -100.93468], [25.55515, -100.93479], [25.55503, -100.93462], [25.55515, -100.93451]],
            'centro': [25.55515, -100.93466]
        },
        {
            'edifcolor': 'green','edifill': 'green',
            'nombre': 'Cafeteria UTC 1',
            'descripcion': 'Descripción de Cafeteria UTC 1',
            'imagen_url': 'img/cafeteria1.webp',
            'coordenadas': [[25.55501, -100.93408], [25.55482, -100.93430], [25.55473, -100.93421], [25.55491, -100.93399]],
            'centro': [25.55485, -100.93415]
        },
        {
            'edifcolor': 'red','edifill': 'red',
            'nombre': 'Edificio 1',
            'descripcion': 'Descripción del Edificio 1',
            'imagen_url': 'img/Edificio_1.webp',
            'coordenadas': [[25.55527, -100.93369], [25.55545, -100.93352], [25.55575, -100.93393], [25.55556, -100.93409]],
            'centro': [25.55550, -100.93380]
        },
        {
            'edifcolor': '#00FFFF','edifill': '#00FFFF',
            'nombre': 'Laboratorio de 7A',
            'descripcion': 'Descripción del Laboratorio de PLC',
            'imagen_url': 'img/Laboratorio_7A.webp',
            'coordenadas': [[25.55573, -100.93424], [25.55586, -100.93411], [25.55615, -100.93447], [25.55602, -100.93461]],
            'centro': [25.55593, -100.93435]
        },
        {
            'edifcolor': 'gray','edifill': 'gray',
            'nombre': 'Caceta 1',
            'descripcion': 'Descripción de Caceta 1',
            'imagen_url': 'img/Caseta_1.webp',
            'coordenadas': [[25.55821, -100.93682], [25.55815, -100.93672], [25.55805, -100.93682], [25.55812, -100.93691]],
            'centro': [25.55815, -100.93682]
        },
        {
            'edifcolor': 'gray','edifill': 'gray',
            'nombre': 'Caceta 2',
            'descripcion': 'Descripción de Caceta 2',
            'imagen_url': 'img/Caseta_2.webp',
            'coordenadas': [[25.55606, -100.93464], [25.55613, -100.93457], [25.55624, -100.93470], [25.55616, -100.93477]],
            'centro': [25.55616, -100.93469]
        },
        {
            'edifcolor': 'red','edifill': 'white',
            'nombre': 'Oxxo',
            'descripcion': 'Descripción de Oxxo',
            'imagen_url': 'img/Oxxo.webp',
            'coordenadas': [[25.55777, -100.93619], [25.55785, -100.93613], [25.55776, -100.93602], [25.55769, -100.93610]],
            'centro': [25.55777, -100.93612]
        },
        {
            'edifcolor': 'blue','edifill': 'blue',
            'nombre': 'Papeleria',
            'descripcion': 'Descripción de Papeleria',
            'imagen_url': 'img/papeleriautc.webp',
            'coordenadas': [[25.55700, -100.93713], [25.55708, -100.93709], [25.55704, -100.93701], [25.55697, -100.93706]],
            'centro': [25.55702, -100.93708]
        },
        {
            'edifcolor': 'green','edifill': 'green',
            'nombre': 'Campo De Fútbol',
            'descripcion': 'Descripción de Campo De Fútbol',
            'imagen_url': 'img/futbol.webp',
            'coordenadas': [[25.55871, -100.93793], [25.55835, -100.93763], [25.55819, -100.93786], [25.55855, -100.93816]],
            'centro': [25.55843, -100.93790]
        },
        {
            'edifcolor': 'green','edifill': 'green',
            'nombre': 'Campo de Softbol',
            'descripcion': 'Descripción de Campo de Softbol',
            'imagen_url': 'img/softbol.webp',
            'coordenadas': [[25.55886, -100.93881], [25.55844, -100.93925], [25.55796, -100.93869], [25.55848, -100.93837]],
            'centro': [25.55842, -100.93879]
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
        email = request.POST.get('email')

        if password1 and password2 and username:
            if password1 == password2:
                try:
                    newUser = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, email=email, is_active=0)
                    newUser.save()
                    return JsonResponse({'success': True, 'message': '🥳🥳🥳 <br>Usuario creado<br> Tu cuenta esta <u>INACTIVA</u>'}, status=200)
                except IntegrityError:
                    return JsonResponse({'success': False, 'message': f'El usuario <u>{username}</u> ya existe 😯'}, status=400)
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
        databaseall = Database.objects.all()
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
    num_blogs = models.Articulos.objects.filter().count()
    num_preguntas = models.Database.objects.filter().count()
    user = request.user
    users = User.objects.filter()
    blogs_all = models.Articulos.objects.filter()
    banners_all = models.Banners.objects.all()
    total_banners = banners_all.count()

    # Procesar la creación de usuario
    if request.method == 'POST':
        username = request.POST.get('username')
        is_staff = request.POST.get('is_staff', False)
        is_active = request.POST.get('is_active', False)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username:
            # Crear el usuario
            new_user = User.objects.create_user(username=username, is_staff=is_staff, is_active=is_active,
            first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)
            new_user.save()
            return redirect('vista_programador')

    return render(request, 'administracion/vista_programador.html', {
        'num_blogs': num_blogs,
        'num_preguntas': num_preguntas,
        'user': user,
        'blogs_all': blogs_all,
        'users': users,
        'banners_all': banners_all,
        'total_banners': total_banners,
    })

# def para responder preguntas
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