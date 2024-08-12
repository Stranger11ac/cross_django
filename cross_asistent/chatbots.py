from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import speech_recognition as sr
from django.db.models import Q
from pathlib import Path
from gtts import gTTS
from . import models
import threading
import requests
import openai
import json
import spacy

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

recognized_texts = []
is_recognizing = False
recognition_thread = None

def speekText():
    global is_recognizing, recognized_texts
    r = sr.Recognizer()
    recognized_texts = []
    while is_recognizing:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("Por favor, hable ahora...")
                audio2 = r.listen(source2)
                recognized_text = r.recognize_google(audio2, language='es-ES')
                recognized_text = recognized_text.lower().strip()
                print("Dijiste:", recognized_text)
                recognized_texts.append(recognized_text)
        except sr.RequestError as e:
            print(f"No se pueden solicitar resultados; {e}")
        except sr.UnknownValueError:
            print("Ocurrió un error desconocido")
    
@csrf_exempt
def start_recognition(request):
    global is_recognizing, recognition_thread
    if request.method == 'POST' and not is_recognizing:
        is_recognizing = True
        recognition_thread = threading.Thread(target=speekText)
        
        recognition_thread.start()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Recognition already started or invalid request'})

@csrf_exempt
def stop_recognition(request):
    global is_recognizing, recognition_thread, recognized_texts
    if request.method == 'POST' and is_recognizing:
        is_recognizing = False
        if recognition_thread:
            recognition_thread.join()

        if recognized_texts:
            question = " ".join(recognized_texts)
            response = requests.post(
                'http://localhost:8000/recognized-text/',
                json={'question': question}
            )
            response_data = response.json()  # Obtener la respuesta JSON

            if isinstance(response_data, dict):
                answer = response_data.get('answer', {})
            else:
                answer = {}

            combined_response = {
                'status': 'success',
                'response': {
                    'question': question,
                    'chatbot_answer': answer
                }
            }
            
            return JsonResponse(combined_response)
        else:
            return JsonResponse({'status': 'success', 'message': 'No se reconoció ningún texto.'})

    return JsonResponse({'status': 'error', 'message': 'Recognition not started or invalid request'})


@csrf_exempt
def recognized_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            
            if not question:
                return JsonResponse({'success': False, 'message': 'Pregunta vacía.'})            
            # Procesa la pregunta con el chatbot
            response = chatbot(request)
            
            # Aquí asumimos que `chatbot` devuelve un JsonResponse, por lo tanto no es necesario
            # crear otro JsonResponse alrededor de la respuesta.
            return response
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error en el formato del JSON.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

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

def synthesize_speech(text, file_name):
    tts = gTTS(text=text, lang='es')
    speech_file_path = Path("cross_asistent/static/audio") / f"{file_name}.mp3"
    tts.save(speech_file_path)
    return speech_file_path

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
    print(f"Similares: {cosine_similarities}")
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

    print(f"score{score}")
    return score
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()

            if not question:
                return JsonResponse({'success': False, 'message': 'Pregunta vacía.'})

            # Verifica respuestas simples
            for clave, respuesta in respuestas_simples.items():
                if clave in question:
                    return JsonResponse({'success': True, 'answer': {'informacion': respuesta}})

            # Procesa la pregunta
            pregunta_procesada = process_question(question)
            entidades = extract_entities(question)
            palabras_clave = pregunta_procesada.split()
            query = create_query(palabras_clave, entidades)
                        
            coincidencias = models.Database.objects.filter(query)
            mejor_coincidencia = None
            mejor_puntuacion = -1
            
            for coincidencia in coincidencias:
                puntuacion = score_result(coincidencia, palabras_clave, entidades, pregunta_procesada)
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_coincidencia = coincidencia

            if mejor_coincidencia:
                informacion = mejor_coincidencia.informacion
                system_prompt = f"Eres un asistente de la Universidad Tecnologica de Coahuila. Responde la pregunta con esta información encontrada: {informacion}"
                answer = chatgpt(question, system_prompt)

                respuesta = {
                    "titulo": mejor_coincidencia.titulo,
                    "informacion": answer,
                    "redirigir": mejor_coincidencia.redirigir,
                    "imagenes": mejor_coincidencia.imagen.url.replace("/cross_asistent", "") if mejor_coincidencia.imagen else None
                }

                audio_path = synthesize_speech(answer, "respuesta_asistente")
                respuesta["audio_url"] = f"/static/audio/{audio_path.name}"
                
                print(f"Respuesta {respuesta}")
                return JsonResponse({'success': True, 'answer': respuesta})

            else:
                respuesta = {
                    "informacion": "¿Podrías ser más específico en tu pregunta? No logré entender completamente lo que necesitas."
                    if len(palabras_clave) == 0 and len(entidades) == 0
                    else "Lo siento, no encontré información relevante."
                }
                return JsonResponse({'success': True, 'answer': respuesta})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Error en el formato del JSON.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
