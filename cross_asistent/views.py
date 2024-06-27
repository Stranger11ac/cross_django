from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseForbidden
from django.db import IntegrityError, models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.apps import apps
from .forms import BannersForm, CSVUploadForm
from . import models

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.http import JsonResponse

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import nltk
import openai
import json
import csv
import os

# openai.api_key = ""

# chat_history = []

# while True:
#     prompt = input("Enter a prompt: ")
#     if prompt == "exit":
#         break
#     else:
#         chat_history.append({"role": "user", "content": prompt})

#         response_iterator = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages = chat_history,
#             stream=True,
#             max_tokens=150,
#         )

#         collected_messages = []

#         for chunk in response_iterator:
#             chunk_message = chunk['choices'][0]['delta']  # extract the message
#             collected_messages.append(chunk_message)  # save the message
#             full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
#             print(full_reply_content)

#             # clear the terminal
#             print("\033[H\033[J", end="")

#         chat_history.append({"role": "assistant", "content": full_reply_content})
#         # print the time delay and text received
#         full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
#         print(f"GPT: {full_reply_content}")


def index(request):
    if not request.user.is_staff:
        logout(request)
    banners_all = models.Banners.objects.all()
    return render(request, 'index.html', {
        'banners': banners_all,
        'active_page': 'inicio'
    })

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def chatgpt(question, instructions):
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

def process_question(pregunta):
    pregunta = pregunta.lower().strip()
    pregunta = "".join([c for c in pregunta if c.isalnum() or c.isspace()])
    tokens = word_tokenize(pregunta)
    stop_words = set(stopwords.words('spanish'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    pregunta_procesada = " ".join(tokens)
    print(pregunta_procesada)

    return pregunta_procesada

def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')

            # Preprocesar la pregunta
            pregunta_procesada = process_question(question)

            # Obtener todas las entradas de la base de datos
            todas_entradas = models.Database.objects.all()

            # Crear una lista de textos de la base de datos
            textos_db = [entrada.informacion for entrada in todas_entradas]

            # Vectorizar las preguntas y las entradas de la base de datos
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(textos_db + [pregunta_procesada])

            # Calcular la similitud de coseno entre la pregunta y las entradas de la base de datos
            cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

            # Encontrar la entrada con la mayor similitud
            mejor_coincidencia_idx = int(np.argmax(cosine_similarities))
            mejor_coincidencia = todas_entradas[mejor_coincidencia_idx]

            if mejor_coincidencia:
                system_prompt = f"Utiliza emojis sutilmente. Eres un asistente de la Universidad Tecnologica de Coahuila. Aquí está la información encontrada: {mejor_coincidencia.informacion}"
                answer = chatgpt(question, system_prompt)

                respuesta = {
                    "titulo": mejor_coincidencia.titulo,
                    "informacion": answer,
                    "redirigir": mejor_coincidencia.redirigir,
                    "documentos": mejor_coincidencia.documentos.url if mejor_coincidencia.documentos else None,
                    "imagenes": mejor_coincidencia.imagenes.url if mejor_coincidencia.imagenes else None
                }
            else:
                respuesta = {
                    "informacion": 'Ups! 😥😯😬 <br>Al parecer no encontre informacion de lo que me pides.',
                }

            return JsonResponse({'success': True, 'answer': respuesta})
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

def crear_pregunta(request):
    quest_all = models.Database.objects.all()
    
    if request.method == "POST":
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                tituloPOST = data['pregunta']
                categoria_preguntas = models.Categorias.objects.get(id=1) 

                pregunta = models.Database(titulo=tituloPOST, categoria=categoria_preguntas)
                pregunta.save()

                return JsonResponse({'success': True, 'message': 'Gracias por tu pregunta ❤️💕😁👍 '}, status=200)
            except Exception as e:
                print(f'Hay un error en: {e}')
                return JsonResponse({'success': False, 'message': 'Ups! 😥😯 hubo un error y tu pregunta no se pudo registrar. por favor intente de nuevo mas tarde.'}, status=400)
        else:
            print('error, no JSON')
            return JsonResponse({'success': False, 'message': 'Error: no se permite este tipo de archivo '}, status=400)
    return render(request, 'frecuentes.html', {'quest_all': quest_all})

def blog(request):
    if not request.user.is_staff:
        logout(request)
    blogs = models.Articulos.objects.all()
    return render(request, 'blog.html', {
        'blogs_all': blogs,
        'active_page': 'blog'
    })

def mostrar_blog(request, Articulos_id):
    if not request.user.is_staff:
        logout(request)
    Articulos = models.Articulos.objects.filter(pk=Articulos_id)
    return render(request, 'mostrar_blogs.html', {'Articulos': Articulos})

def map(request):
    if not request.user.is_staff:
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
    if not request.user.is_staff:
        logout(request)
    return render(request, 'about.html', {
        'active_page': 'about'
    })

# Administracion ----------------------------------------------------------
def create_user(first_name, last_name, username, email, password1, password2=None, is_staff=False, is_active=False):
    if not (password1 and username and email):
        return {'success': False, 'message': 'Datos incompletos 😅'}
    if password2 is not None and password1 != password2:
        return {'success': False, 'message': 'Las contraseñas no coinciden 😬'}
    if User.objects.filter(username=username).exists():
        return {'success': False, 'message': f'El usuario <u>{username}</u> ya existe 😯'}
    if User.objects.filter(email=email).exists():
        return {'success': False, 'message': f'El correo electrónico <u>{email}</u> ya está registrado 😯'}

    try:
        new_user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password1,
            is_staff=is_staff,
            is_active=is_active,
        )
        new_user.save()
        aviso=''
        if password2 is not None:
            aviso = '<br>Tu cuenta está <u>INACTIVA</u>'
        return {'success': True, 'message': f'Usuario creado exitosamente 🥳😬🎈 {aviso}'}
    except IntegrityError:
        return {'success': False, 'message': 'Ocurrió un error durante el registro. Intente nuevamente.'}

@never_cache
def singuppage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        response = create_user(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password1=request.POST.get('password1'),
            password2=request.POST.get('password2'),
        )
        response['functions'] = 'singup'
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)
    else:
        logout(request)
        return render(request, 'singin')

@never_cache
def singinpage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        usernamePOST = request.POST.get('username')
        passwordPOST = request.POST.get('password')
        
        try: user = User.objects.get(username=usernamePOST)
        except User.DoesNotExist: user = None
        if user is not None:
            if not user.is_active:
                return JsonResponse({'success': False, 'functions': 'singin', 'message': '🧐😥😯 UPS! <br> Al parecer tu cuenta esta <u>Inactiva</u>. Tu cuenta será activada si estas autorizado'}, status=400)
            
            user = authenticate(request, username=usernamePOST, password=passwordPOST)
            if user is None:
                return JsonResponse({'success': False, 'functions': 'singin', 'message': 'Revisa el usuario o contraseña 😅.'}, status=400)
            else:
                login(request, user)
                pageRedirect = reverse('vista_admin')
                if user.is_staff:
                    pageRedirect = reverse('vista_programador')
                return JsonResponse({'success': True, 'functions': 'singin', 'redirect_url': pageRedirect}, status=200)
        else:
            return JsonResponse({'success': False, 'functions': 'singin', 'message': 'Usuario no registrado 😅. Vrifica tu nombre de usuario'}, status=400)
    else:
        logout(request)
        return render(request, 'admin/singin.html', {
            'active_page': 'singin'
        })

@login_required
@never_cache
def singoutpage(request):
    logout(request)
    return redirect('singin')

# def consulTabla(request):
#     if request.user.is_staff:
#         # Obtener nombres de todas las tablas del modelo
#         all_models = apps.get_models()
#         cross_assistent_models = [model for model in all_models if model._meta.app_label == 'cross_assistent']
        
#         # Imprimir todos los modelos y los modelos de la app cross_assistent para depuración
#         print(f"Todos los modelos: {[model._meta.object_name for model in all_models]}")
#         print(f"Modelos de cross_assistent: {[model._meta.object_name for model in cross_assistent_models]}")
        
#         data_table = [model._meta.object_name for model in cross_assistent_models]
#         return render(request, 'admin/vista_programador.html', {'data_table': data_table})
#     else:
#         return HttpResponseForbidden()

@login_required
@never_cache
def export_database(request):
    now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M%S')
    if request.user.is_staff:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="UTC_database_{now}.csv"'
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
def import_database(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            csv_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(csv_file)
            next(reader)  # Omitir la fila de encabezado
            for row in reader:
                categoria, _ = models.Categorias.objects.get_or_create(categoria=row[0])
                # Crear la instancia del modelo
                models.Database.objects.create(
                    categoria=categoria,
                    titulo=row[1],
                    informacion=row[2],
                    redirigir=row[3],
                    frecuencia=int(row[4]),
                    documentos=row[5],
                    imagenes=row[6],
                    fecha_modificacion=row[7]
                )
            # Redirigir a la vista programador después de procesar el formulario
        return JsonResponse({'success': True, 'functions': 'others', 'message': 'Base de datos importada correctamente ✔'}, status=200)
    else:
        form = CSVUploadForm()
    
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
    return render(request, 'admin/vista_admin.html', context)

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
    
    if request.method == 'POST':
        response = create_user(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password1=request.POST.get('password'),
            is_staff=request.POST.get('is_staff', False),
            is_active=request.POST.get('is_active', False),
        )
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)

    return render(request, 'admin/vista_programador.html', contexto)

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
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        
        if username:
            user.username = username
        if password:
            user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.save()
        return redirect('vista_programador')
    return redirect('vista_programador')

def mapa2(request):
    return render(request, 'mapa2.html')

# te manda a la vista para crear el blog siendo staff
@login_required
@never_cache
def admin_blogs(request):
    return render(request, 'admin/blogs.html')

# crea el archivo del blog
@login_required
@never_cache
def crear_articulo(request):
    if request.method == 'POST':
        try:
            tituloPOST = request.POST.get('titulo')
            autorPOST = request.POST.get('autor')
            contenidoPOST = request.POST.get('contenidoWord')
            encabezadoPOST = request.FILES.get('encabezadoImg')

            articulo = models.Articulos(
                titulo=tituloPOST,
                contenido=contenidoPOST,
                autor=autorPOST,
                encabezado=encabezadoPOST
            )
            articulo.save()

            return JsonResponse({'success': True, 'message': 'Excelente 🥳🎈🎉. Tu articulo ya fue publicado. Puedes editarlo cuando gustes. 🧐😊'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ocurrio un error😯😥 <br>{str(e)}'}, status=400)
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

# sube la imagen que viene dentro del contenido del blog
@login_required
@never_cache
def upload_image(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES['file']
            imagen_articulo = models.ImagenArticulo(imagen=image_file)
            imagen_articulo.save()
            image_url = imagen_articulo.imagen.url.replace("/cross_asistent", "")

            return JsonResponse({'location': image_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Error al subir la imagen'}, status=400)

#Consulta para informacion del Mapa##################
def obtenerinfoEdif(request):
        categoria_mapa = models.Categorias.objects.get(categoria="Mapa")
        articulos_mapa = models.Mapa.objects.filter(categoria=categoria_mapa)
        
        return render(request, 'admin/mapa_form.html', {'articulos_mapa': articulos_mapa})

def obtenerEdificio(request):
    if request.method == 'GET':
        edificio_id = request.GET.get('id')
        if (edificio_id):
            edificio = get_object_or_404(models.Mapa, id=edificio_id)
            data = {
                'id': edificio.id,
                'titulo': edificio.titulo,
                'informacion': edificio.informacion,
                'color': edificio.color,
                'p1_polygons': edificio.p1_polygons,
                'p2_polygons': edificio.p2_polygons,
                'p3_polygons': edificio.p3_polygons,
                'p4_polygons': edificio.p4_polygons,
                'imagen_url': edificio.imagenes.url if edificio.imagenes else None,
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def crearEditarMapa(request):
    if request.method == 'POST':
        edificio_id = request.POST.get('edificio_id')
        titulo = request.POST.get('titulo')
        informacion = request.POST.get('informacion')
        color = request.POST.get('color')
        p1_polygons = request.POST.get('p1_polygons')
        p2_polygons = request.POST.get('p2_polygons')
        p3_polygons = request.POST.get('p3_polygons')
        p4_polygons = request.POST.get('p4_polygons')
        categoria = models.Categorias.objects.get(categoria="Mapa")
        imagen = request.FILES.get('imagenes')

        if edificio_id:
            # Editar edificio existente
            edificio = get_object_or_404(models.Mapa, id=edificio_id)
            edificio.titulo = titulo
            edificio.informacion = informacion
            edificio.color = color
            edificio.p1_polygons = p1_polygons
            edificio.p2_polygons = p2_polygons
            edificio.p3_polygons = p3_polygons
            edificio.p4_polygons = p4_polygons
            if imagen:
                edificio.imagenes = imagen
            edificio.save()
        else:
            # Crear nuevo edificio
            models.Mapa.objects.create(
                categoria=categoria,
                titulo=titulo,
                informacion=informacion,
                color=color,
                p1_polygons=p1_polygons,
                p2_polygons=p2_polygons,
                p3_polygons=p3_polygons,
                p4_polygons=p4_polygons,
                imagenes=imagen
            )
    return redirect('consultaMap')

# subir banners###########################
@login_required
def upload_banner(request):
  if request.method == 'POST':
    form = BannersForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return render(request, 'admin/banners.html', context={'form': form})
  else:
    form = BannersForm()
  context = {'form': form}
  return render(request, 'admin/banners.html', context)

@login_required
@never_cache
def ver_perfil(request):
    return render(request, 'admin/perfil.html')