from sklearn.feature_extraction.text import TfidfVectorizer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from sklearn.metrics.pairwise import cosine_similarity
from django.views.decorators.cache import never_cache
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from . import models
import datetime
import openai
import spacy
import json

# ChatBot ----------------------------------------------------------
# Cargar el modelo de lenguaje español
# analizar texto en aplicaciones de procesamiento de lenguaje natural.
nlp = spacy.load("es_core_news_sm")
# Diccionario de respuestas simples predefinidas
respuestas_simples = {
    "contacto": "Puedes contactarnos al teléfono (844)288-38-00 ☎️",
}
palabras_clave = ["hola", "servicios", "escolares", "donde", "esta"]  # Ejemplo de palabras clave

# Plantilla links programador / administrador ----------------------------------------------------------
pages = [
        {'name': 'banner', 'url': 'upload_banner', 'display_name': 'Banners', 'icon': 'fa-solid fa-image'},
        {'name': 'database', 'url': 'database_page', 'display_name': 'Database', 'icon': 'fa-solid fa-database'},
        {'name': 'blog', 'url': 'create_blog', 'display_name': 'Blogs', 'icon': 'fa-solid fa-newspaper'},
        {'name': 'mapa', 'url': 'update_mapa', 'display_name': 'Mapa', 'icon': 'fa-solid fa-map-location-dot'},
        {'name': 'calendario', 'url': 'calendario_page', 'display_name': 'Calendario', 'icon': 'fa-solid fa-calendar-days'},
    ]

def chatgpt(question, instructions):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
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
    doc = nlp(pregunta.lower().strip())
    tokens = [token.lemma_ for token in doc if (not token.is_stop and token.is_alpha) or token.text in palabras_clave]
    pregunta_procesada = " ".join(tokens)
    print(f"Pregunta procesada: {pregunta_procesada}")
    return pregunta_procesada

def extract_entities(pregunta):
    doc = nlp(pregunta)
    entities = [ent.text for ent in doc.ents]
    print(f"Entidades nombradas: {entities}")
    return entities

def create_query(palabras_clave, entities):
    query = Q()
    for palabra in palabras_clave:
        query |= Q(titulo__icontains=palabra) | Q(informacion__icontains=palabra)
    for entidad in entities:
        query |= Q(titulo__icontains=entidad) | Q(informacion__icontains=entidad)
    return query

def calculate_tfidf_similarity(pregunta, textos):
    vectorizer = TfidfVectorizer().fit_transform([pregunta] + textos)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    return cosine_similarities

def score_result(result, palabras_clave, entities, pregunta_procesada):
    score = 0
    texto_completo = f"{result.titulo.lower()} {result.informacion.lower()}"
    
    for palabra in palabras_clave:
        if palabra in result.titulo.lower():
            score += 3
        if palabra in result.informacion.lower():
            score += 2

    for entidad in entities:
        if entidad in result.titulo.lower():
            score += 4
        if entidad in result.informacion.lower():
            score += 3
    
    tfidf_sim = calculate_tfidf_similarity(pregunta_procesada, [texto_completo])[0]
    score += tfidf_sim * 5 

    return score

def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            
            for clave, respuesta in respuestas_simples.items():
                if clave in question:
                    return JsonResponse({'success': True, 'answer': {'informacion': respuesta}})
            
            pregunta_procesada = process_question(question)
            entidades = extract_entities(question)
            
            palabras_clave = pregunta_procesada.split()
            query = create_query(palabras_clave, entidades)
            
            coincidencias = models.Database.objects.filter(query)
            
            mejor_coincidencia = None
            mejor_puntuacion = -1  # Asegura que la puntuación sea un número
            
            for coincidencia in coincidencias:
                puntuacion = score_result(coincidencia, palabras_clave, entidades, pregunta_procesada)
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_coincidencia = coincidencia

            print(f"Mejor coincidencia: {mejor_coincidencia}")
            print(f"Mejor puntuación: {mejor_puntuacion}")
            
            if mejor_coincidencia:
                informacion = mejor_coincidencia.informacion
                system_prompt = f"Utiliza emojis sutilmente. Eres un asistente de la Universidad Tecnologica de Coahuila. Responde la pregunta con esta información encontrada: {informacion}"
                answer = chatgpt(question, system_prompt)
                print(f"Informacion: {informacion}")

                respuesta = {
                    "titulo": mejor_coincidencia.titulo,
                    "informacion": answer,
                    "redirigir":  mejor_coincidencia.redirigir,
                    "imagenes": mejor_coincidencia.imagenes.url.replace("cross_asistent/", "") if mejor_coincidencia.imagenes else None
                }
                print(f"Respuesta JSON: {respuesta}")  
                return JsonResponse({'success': True, 'answer': respuesta,})

            else:
                if len(palabras_clave) == 0 and len(entidades) == 0:
                    respuesta = {"informacion": "¿Podrías ser más específico en tu pregunta? No logré entender completamente lo que necesitas."}
                else:
                    respuesta = {"informacion": "Lo siento, no encontré información relevante."}
                
                return JsonResponse({'success': True, 'answer': respuesta})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error en el formato del JSON.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Editar Perfil ----------------------------------------------------------
def editar_perfil(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_auth = request.user
        user_perfil = request.user.userprofile
        
        fNamePOST = request.POST.get('first_nameChanged')
        lNamePOST = request.POST.get('last_nameChanged')
        usernamePOST = request.POST.get('usernameChanged')
        emailPOST = request.POST.get('emailChanged')
        firmaPOST = request.POST.get('firmaBlog')
        picturePOST = request.FILES.get('userPictureChanged')
        delPicturePOST = request.POST.get('deletePicture')
        PasswordPOST = request.POST.get('passwordSend')
        newPasswordPOST = request.POST.get('confNewPass')
        
        if not user_auth.check_password(PasswordPOST):
            return JsonResponse({'success': False, 'message': 'La contraseña actual es incorrecta.'}, status=400)
        
        if emailPOST and User.objects.filter(email=emailPOST).exclude(id=user_auth.id).exists():
            return JsonResponse({'success': False, 'message': f'El correo electrónico "{emailPOST}" ya está en uso por otra cuenta. 🤔😯😯🧐'}, status=400)
        
        if usernamePOST and usernamePOST != user_auth.username:
            if User.objects.filter(username=usernamePOST).exists():
                return JsonResponse({'success': False, 'message': 'El nombre de usuario ya está en uso.'}, status=400)
            user_auth.username = usernamePOST
        
        with transaction.atomic():
            if fNamePOST:
                user_auth.first_name = fNamePOST
            
            if lNamePOST:
                user_auth.last_name = lNamePOST
            
            if emailPOST:
                user_auth.email = emailPOST
            
            if firmaPOST:
                user_perfil.blog_firma = firmaPOST
            
            if picturePOST:
                user_perfil.profile_picture = picturePOST
            
            if delPicturePOST == 'on':
                user_perfil.profile_picture.delete()
                user_perfil.profile_picture = None
            
            if newPasswordPOST:
                if PasswordPOST == newPasswordPOST:
                    return JsonResponse({'success': False, 'message': 'La nueva contraseña no puede ser igual a la actual.'}, status=400)
                user_auth.set_password(newPasswordPOST)
                user_perfil.passwoed_update = datetime.date.today()

            user_auth.save()
            user_perfil.save()
        return JsonResponse({'success': True, 'message': 'Tus Datos Se guardaron exitosamente. 🥳😋🤘🎉🎈', 'position': 'top'}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=400)

# usuarios ----------------------------------------------------------
def create_newuser(first_name, last_name, username, email, password1, password2=None, is_staff=False, is_active=False):
    if not (password1 and username and email):
        return {'success':False, 'message':'Datos incompletos 😅'}
    if password2 is not None and password1 != password2:
        return {'success':False, 'message':'Las contraseñas no coinciden 😬'}
    if User.objects.filter(username=username).exists():
        return {'success':False, 'message':f'El usuario <u>{username}</u> ya existe. 😯🤔 <br>Te recomiendo utilizar uno distinto', 'valSelector':'usernameSelect'}
    if User.objects.filter(email=email).exists():
        return {'success':False, 'message':f'El correo electrónico <u>{email}</u> ya está registrado 😯<br>Te recomiendo utilizar uno distinto', 'valSelector':'emailSelect'}

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
            aviso = '<br>Tu cuenta está <u>Inhabilitada</u> 😯😬'
        return {'success': True, 'message': f'Usuario creado exitosamente 🥳🎈 {aviso}'}
    except IntegrityError:
        return {'success': False, 'message': 'Ocurrió un error durante el registro. Intente nuevamente.'}

# (programacion) ----
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
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': 'Usuario eliminado exitosamente.', 'icon': 'warning'}, status=200)
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

# Banners ----------------------------------------------------------
@login_required
@never_cache
def banner_update(request, banner_id):
    banner = get_object_or_404(models.Banners, id=banner_id)
    if request.method == 'POST':        
        banner.solo_imagen = request.POST.get('soloImagen')
        if banner.solo_imagen == None:
            banner.solo_imagen = False
            
        new_image = request.FILES.get('imagen')
        if not new_image == None:
            banner.imagen = new_image
        banner.titulo = request.POST.get('contenidoWord')
        banner.descripcion = request.POST.get('descripcion')
        banner.redirigir = request.POST.get('redirigir')
        if banner.expiracion:
            banner.expiracion = request.POST.get('expiracion')
        banner.save()
        
        return JsonResponse({
            'success': True,
            'functions': 'reload',
            'message': f'El banner <u>{banner.titulo}</u> fue modificado exitosamente 🥳🎉🎈.'
        }, status=200)
    
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

@login_required
@never_cache
def banner_delete(request, banner_id):
    if request.method == 'POST':
        banner = get_object_or_404(models.Banners, id=banner_id)
        banner.delete()
        icon = 'warning'
        return JsonResponse({'success': True, 'functions': 'reload', 'message': 'Banner eliminado exitosamente.', 'icon': icon}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

@login_required
@never_cache
def banners_visibility_now(request):
    if request.method == 'POST':
        banneridPOST = request.POST.get('banner_id')
        if banneridPOST:
            expired_banners = models.Banners.objects.filter(id=banneridPOST)
            update_visibility = request.POST.get('banner_visible')
            returnJson = {'success': True, 'functions':'reload', 'message':f'Se cambio la visibilidad del banner <span>#{banneridPOST}</span> exitosamente 🫡🥳🎉.'}
        else:
            now = timezone.now()
            expired_banners = models.Banners.objects.filter(expiracion__lte=now, visible=True)
            update_visibility = False
            returnJson = {'status': 'success'}
            
        for banner in expired_banners:
            banner.visible = update_visibility
            banner.save()
        return JsonResponse(returnJson, status=201)
    return('upload_banner')

# Base de Datos ----------------------------------------------------------
@login_required
@never_cache
def createDatabase(request):
    if request.method == 'POST':
        try:
            categoriaIdPOST = request.POST.get('categoria')
            categoria = models.Categorias.objects.get(id=categoriaIdPOST) if categoriaIdPOST else None
            tituloPOST = request.POST.get('titulo')
            informacionPOST = request.POST.get('informacion')
            redirigirPOST = request.POST.get('redirigir')
            documentosPOST = request.FILES.get('documentos')
            imagenesPOST = request.FILES.get('imagenes')
            
            if categoria and categoria.categoria == 'Preguntas':
                frecuenciaPOST = 1
            else:
                frecuenciaPOST = 0
            
            models.Database.objects.create(
                categoria=categoria,
                titulo=tituloPOST,
                informacion=informacionPOST,
                redirigir=redirigirPOST,
                frecuencia=frecuenciaPOST,
                documentos=documentosPOST,
                imagenes=imagenesPOST,
                evento_lugar='',
                evento_className='',
            )
            
            models.Notificacion.objects.create(
                usuario=request.user,
                tipo='Base de Datos',
                mensaje=f'{request.user.username} ha creado un nuevo registro de categoría "{categoria}".',
            )
            return JsonResponse({'success': True, 'message': 'Nuevo registro en la base de datos 🎉🎉🎉', 'position':'top'}, status=200)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ocurrió un error 😯😥 <br>{str(e)}'}, status=400)
    return JsonResponse({'error': 'Método no válido'}, status=400)

# Calendario: Eventos ---------------------
def calendario_eventos(request):
    categoriaGet = get_object_or_404(models.Categorias, categoria="Calendario")
    eventos = models.Database.objects.filter(categoria=categoriaGet).select_related('categoria')
    eventos_json = [{
        'title': evento.titulo,
        'description': evento.informacion,
        'classNames': evento.evento_className,
        'location': evento.evento_lugar,
        'imagen': evento.imagen.url if evento.imagen else '',
        'button': evento.redirigir if evento.redirigir else '',
        'start': evento.evento_fecha_inicio.isoformat() if evento.evento_fecha_inicio else '',
        'end': evento.evento_fecha_fin.isoformat() if evento.evento_fecha_fin else '',
    } for evento in eventos]
    
    return JsonResponse(eventos_json, safe=False)

# Blogs ----------------------------------------------------------
@login_required
@never_cache
def blog_change(request):
    if request.method == 'GET':
        blogIdGET = request.GET.get('id')
        if (blogIdGET):
            blogGet = get_object_or_404(models.Articulos, id=blogIdGET)
            blogEncabezado = blogGet.encabezado
            if blogEncabezado:
                blogEncabezado = blogGet.encabezado.url.replace("cross_asistent/", "")
            else:
                blogEncabezado = ''
            data = {
                'autor': blogGet.autor,
                'titulo': blogGet.titulo,
                'contenido': blogGet.contenido,
                'encabezado': blogEncabezado,
            }
            return JsonResponse(data)
    return JsonResponse({'success': False}, status=400)

@login_required
@never_cache
def blog_delete(request):
    if request.method == 'POST':
        idPOST = request.POST.get('blogIdDelete')
        blogId = get_object_or_404(models.Articulos, id=idPOST)
        blogId.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': f'El blog "{blogId.titulo}" <u>se elimino</u> exitosamente. 😯😬🎉', 'icon': 'warning'}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

# Mapa ----------------------------------------------------------
def mapa_data(request):
    mapas = models.Mapa.objects.all()
    data = []
    for mapa in mapas:
        imagen_qs = models.Database.objects.filter(titulo=mapa.nombre).values_list('imagen', flat=True)
        imagen = imagen_qs.first() if imagen_qs.exists() else None
        
        if imagen:
            imagen = imagen.replace("cross_asistent", "")

        item = {
            "muid": mapa.muid,
            "color": mapa.color,
            "imagen_url": imagen,
            "nombre": mapa.nombre,
            "informacion": mapa.informacion,
            "door_coords": [float(coord) for coord in mapa.door_cords.split(",")],
            "polygons": [
                [float(coord) for coord in mapa.p1_polygons.split(",")],
                [float(coord) for coord in mapa.p2_polygons.split(",")],
                [float(coord) for coord in mapa.p3_polygons.split(",")],
                [float(coord) for coord in mapa.p4_polygons.split(",")],
            ]
        }
        data.append(item)

    return JsonResponse(data, safe=False)

@login_required
@never_cache
def delete_pleaceMap(request):
    if request.method == 'POST':
        sendUid = request.POST.get('muid')
        pleace = get_object_or_404(models.Mapa, muid=sendUid)
        pleace.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': f'Se elimino <u>"{pleace.nombre}"</u> del Mapa exitosamente. 😯😬🎉', 'icon': 'warning'}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

@login_required
@never_cache
def delete_pleaceMap_DB(request):
    if request.method == 'POST':
        sendUid = request.POST.get('muid')
        pleace = get_object_or_404(models.Mapa, muid=sendUid)
        pleace.delete()
        pleaceDB = get_object_or_404(models.Database, muid=sendUid)
        pleaceDB.delete()
        return JsonResponse({'success': True, 'functions': 'reload', 'message': f'Se elimino <u>"{pleace.nombre}"</u> del Mapa y de la Base de Datos exitosamente. ⚠️😯😬🎉', 'icon': 'warning'}, status=200)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=403)

# Preguntas ----------------------------------------------------------
@login_required
@never_cache
def preguntas_deleted(request):
    if request.method == 'POST':
        try:
            quest_id = request.POST.get('question_id')
            pregunta = get_object_or_404(models.Preguntas, id=quest_id)
            pregunta.delete()
            return JsonResponse({'success': True, 'message': f'Pregunta #.{quest_id} eliminada permanentemente. 😯🫡', 'icon': 'warning'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Pregunta #{quest_id} no encontrada.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Acción no permitida.'}, status=400)
