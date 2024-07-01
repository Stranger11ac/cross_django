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
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail

from .forms import BannersForm, CSVUploadForm
from .buildings import edificios
from . import models


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
    banners_modificados = []

    for banner in banners_all:
        imagen_url = banner.imagen.url.replace("/cross_asistent", "")
        banners_modificados.append({
            'id': banner.id,
            'titulo': banner.titulo,
            'descripcion': banner.descripcion,
            'articulo': banner.articulo,
            'imagen': imagen_url,
        })

    return render(request, 'index.html', {
        'banners': banners_modificados,
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
        response['functions'] = 'reload'
        status = 200 if response['success'] else 400
        return JsonResponse(response, status=status)
    else:
        logout(request)
        return render(request, 'singin')

@never_cache
def singinpage(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        login_identifier = request.POST.get('username')  # Puede ser username o email
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=login_identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=login_identifier)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            if not user.is_active:
                return JsonResponse({'success': False, 'functions': 'singin', 'message': '🧐😥😯 UPS! <br> Al parecer tu cuenta esta <u>Inactiva</u>. Tu cuenta será activada si estas autorizado'}, status=400)
            
            user = authenticate(request, username=user.username, password=password)
            if user is None:
                return JsonResponse({'success': False, 'functions': 'singin', 'message': 'Revisa el usuario o contraseña 😅.'}, status=400)
            else:
                login(request, user)
                pageRedirect = reverse('vista_admin')
                if user.is_staff:
                    pageRedirect = reverse('vista_programador')
                return JsonResponse({'success': True, 'functions': 'singin', 'redirect_url': pageRedirect}, status=200)
        else:
            return JsonResponse({'success': False, 'functions': 'singin', 'message': 'Usuario no registrado 😅. Verifica tu nombre de usuario o correo electrónico'}, status=400)
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
        return JsonResponse({'success': True, 'message': 'Base de datos importada correctamente ✔'}, status=200)
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
        response['functions'] = 'reload'
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
def in_active(request):
    if request.method == 'POST' and request.user.is_staff:
        user_id = request.POST.get('user_id')
        action = request.POST.get('actionform')
        userChange = get_object_or_404(User, id=user_id)

        if action == 'activate':
            userChange.is_active = True
            message = f'Usuario "{userChange.username}" activado exitosamente. 😊🎈'
            icon = 'info'
        elif action == 'deactivate':
            userChange.is_active = False
            message = f'Usuario "{userChange.username}" <strong><u>desactivado</u></strong> exitosamente. 😯🧐😬'
            icon = 'warning'
        else:
            return JsonResponse({'success': False, 'message': 'Acción no válida.'}, status=400)

        userChange.save()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': message, 'icon':icon}, status=200)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

@login_required
@never_cache
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        icon = 'warning'
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': 'Usuario eliminado exitosamente.', 'icon': icon}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

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
        return JsonResponse({'success': True, 'message': f'El usuario <u>{username}</u> fue modificado exitosamente 🥳🎉🎈.'}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

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

            return JsonResponse({'success': True, 'functions': 'reload', 'message': 'Excelente 🥳🎈🎉. Tu articulo ya fue publicado. Puedes editarlo cuando gustes. 🧐😊'}, status=200)
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

@login_required
@never_cache
def lista_imagenes(request):
    imagenes = models.ImagenArticulo.objects.all()
    imagenes_modificadas = []

    for imagen in imagenes:
        imagen_url = imagen.imagen.url.replace("/cross_asistent", "")
        imagenes_modificadas.append({
            'id': imagen.id,
            'url': imagen_url
        })

    return render(request, 'admin/blogs_imgs.html', {'imagenes': imagenes_modificadas})


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

def password_reset_request(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        email = request.POST.get('email')
        print(f"Email recibido: {email}")

        if email:
            try:
                user = User.objects.get(email=email)
                print(f"Usuario encontrado: {user}")

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

                subject = "Reestablecer la contraseña"
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                print(f"Enlace de restablecimiento: {reset_link}")

                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                print("Correo enviado exitosamente")

                return JsonResponse({'success': True, 'message': 'Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.'}, status=200)
            except User.DoesNotExist:
                print("Usuario no encontrado")
                return JsonResponse({'success': False, 'message': 'El correo electrónico no está registrado.'}, status=400)
        else:
            print("No se proporcionó correo electrónico")
            return JsonResponse({'success': False, 'message': 'Por favor, ingresa tu correo electrónico.'}, status=400)
    else:
        return render(request, 'reset_pass.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return redirect('password_reset_complete')
            else:
                return render(request, 'password_reset_confirm.html', {'validlink': True, 'error': 'Las contraseñas no coinciden.'})
        else:
            return render(request, 'password_reset_confirm.html', {'validlink': True})
    else:
        return render(request, 'password_reset_confirm.html', {'validlink': False})