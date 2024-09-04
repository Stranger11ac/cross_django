from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from .models import Database
import openai
import spacy
import json

# Cargar el modelo de spaCy una sola vez para mejorar el rendimiento
nlp = spacy.load("es_core_news_sm")
respuestas_simples = {"contacto": "Puedes contactarnos al teléfono (844)288-38-00 ☎️"}
palabras_clave = ["hola", "servicios", "escolares", "donde", "esta"]

now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')

# Función para generar la respuesta utilizando OpenAI
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
    print(f"Prompt Tokens: {response.usage.prompt_tokens}")
    print(f"Completion Tokens: {response.usage.completion_tokens}")
    print(f"Total Tokens: {response.usage.total_tokens}")
    print()
    return response.choices[0].message.content

# Función para calcular la similitud TF-IDF
def calculate_tfidf_similarity(pregunta, textos):
    vectorizer = TfidfVectorizer().fit_transform([pregunta] + textos)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    print(f"Similitud TF-IDF: {cosine_similarities}")
    return cosine_similarities

# Función para crear la consulta a la base de datos
def create_query(palabras_clave, entities):
    query = Q()
    for palabra in palabras_clave:
        query |= Q(titulo__icontains=palabra) | Q(informacion__icontains=palabra)
    for entidad in entities:
        query |= Q(titulo__icontains=entidad) | Q(informacion__icontains=entidad)
    return query

# Función para extraer entidades nombradas de la pregunta
def extract_entities(pregunta):
    doc = nlp(pregunta)
    entities = [ent.text for ent in doc.ents]
    print(f"Entidades nombradas: {entities}")
    print()
    return entities

# Función para procesar la pregunta
def process_question(pregunta):
    pregunta_normalizada = pregunta.lower().strip()
    doc = nlp(pregunta_normalizada)
    tokens = [token.lemma_ for token in doc if (not token.is_stop and token.is_alpha) or token.text in palabras_clave]
    pregunta_procesada = " ".join(tokens)
    print(f"Pregunta procesada: {pregunta_procesada}")
    print()
    return pregunta_procesada

# Función para calcular la puntuación de cada resultado
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

    print(f"Puntuación del resultado: {score}")
    return score

# Función para filtrar y ordenar resultados de la base de datos
def filter_results(pregunta):
    palabras_clave = process_question(pregunta)
    entities = extract_entities(pregunta)
    query = create_query(palabras_clave, entities)

    results = Database.objects.filter(query)
    scored_results = [(result, score_result(result, palabras_clave, entities, process_question(pregunta))) for result in results]
    sorted_results = sorted(scored_results, key=lambda x: x[1], reverse=True)

    return sorted_results

# Función principal del chatbot
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            
            if not question:
                return JsonResponse({'success': False, 'message': 'No puedo responder una pregunta que no existe 🤔🧐😬.'})

            # Verificar si la pregunta tiene una respuesta simple predefinida
            respuesta_simple = next((respuesta for clave, respuesta in respuestas_simples.items() if clave in question), None)
            if respuesta_simple:
                return JsonResponse({'success': True, 'answer': {'informacion': respuesta_simple}})

            # Cachear preguntas frecuentes para mejorar el rendimiento
            cache_key = f"chatbot_{question}"
            cached_response = cache.get(cache_key)
            if cached_response:
                print(f"Respuesta cacheada: {cached_response}")
                print()
                return JsonResponse({'success': True, 'answer': cached_response})

            # Procesar la pregunta y buscar coincidencias en la base de datos
            resultados_filtrados = filter_results(question)
            mejor_coincidencia = resultados_filtrados[0][0] if resultados_filtrados else None

            if mejor_coincidencia:
                informacion = mejor_coincidencia.informacion
                system_prompt = f"Eres Hawky, asistente de la Universidad Tecnologica de Coahuila. Utiliza emojis al final, no saludar. Responde la pregunta con esta información: {informacion}. Hoy: {now}."
                answer = chatgpt(question, system_prompt)

                respuesta = {
                    "titulo": mejor_coincidencia.titulo,
                    "informacion": answer,
                    "redirigir": mejor_coincidencia.redirigir,
                    "blank": True,
                    "imagenes": mejor_coincidencia.imagen.url if mejor_coincidencia.imagen else None
                }

                # Almacenar en cache la respuesta para preguntas futuras similares
                cache.set(cache_key, respuesta, timeout=60*60*24)  # Cache de 24 horas

                print(f"Respuesta generada: {respuesta}")
                print()
                return JsonResponse({'success': True, 'answer': respuesta})

            # Respuesta por defecto si no hay coincidencias
            respuesta_default = {
                "informacion": "Lo siento, no encontré información relacionada con lo que me pides 🤔. Puedes buscar más información en la página de preguntas frecuentes o, si gustas, también puedes enviarnos tus dudas. 😊😁",
                "redirigir": "preguntas_frecuentes/",
                "blank": False,
            }
            return JsonResponse({'success': True, 'answer': respuesta_default})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Ocurrió un error. Al parecer no se permite este método. Código #400'})
        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Error en la clave del JSON: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
