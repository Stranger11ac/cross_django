from django.shortcuts import render, redirect, get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer
from django.contrib.auth.decorators import login_required
from sklearn.metrics.pairwise import cosine_similarity
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from django.conf import settings
from django.db.models import Q
from . import models
import openai
import spacy
import json


# ChatBot ---------------------------------------------------
# Cargar el modelo de lenguaje español
# analizar texto en aplicaciones de procesamiento de lenguaje natural.
nlp = spacy.load("es_core_news_sm")
# Diccionario de respuestas simples predefinidas
respuestas_simples = {
    "contacto": "Puedes contactarnos al teléfono (844)288-38-00 ☎️",
}
palabras_clave = ["hola", "servicios", "escolares", "donde", "esta"]  # Ejemplo de palabras clave


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
                    "imagenes": mejor_coincidencia.imagenes.url.replace("/cross_asistent", "") if mejor_coincidencia.imagenes else None
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

# Mapa ---------------------------------------------------
def mapa_data(request):
    mapas = models.Mapa.objects.all()
    features = []
    for mapa in mapas:
        
        imagen_qs = models.Database.objects.filter(titulo=mapa.nombre).values_list('imagenes', flat=True)
        imagen = imagen_qs.first() if imagen_qs.exists() else None
        
        feature = {
            "type": "Feature",
            "properties": {
                "color": mapa.color,
                "imagen_url": imagen,
                "nombre": mapa.nombre,
                "informacion": mapa.informacion,
                "door": [float(coord) for coord in mapa.door_cords.split(",")],
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [float(coord) for coord in mapa.p1_polygons.split(",")],
                        [float(coord) for coord in mapa.p2_polygons.split(",")],
                        [float(coord) for coord in mapa.p3_polygons.split(",")],
                        [float(coord) for coord in mapa.p4_polygons.split(",")],
                        [float(coord) for coord in mapa.p1_polygons.split(",")]
                    ]
                ],
            },
        }
        features.append(feature)

    geojsonEdificios = {
        "type": "FeatureCollection",
        "features": features,
    }
    return JsonResponse(geojsonEdificios)


# Crear nuevo usuario ---------------------------------------------
def create_newuser(first_name, last_name, username, email, password1, password2=None, is_staff=False, is_active=False):
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
    

# Modificar usuario (programador) --------------------------------------------------------
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

