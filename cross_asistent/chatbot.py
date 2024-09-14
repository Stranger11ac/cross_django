from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from .models import Database
import openai
import spacy
import json


now = timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H%M')

nlp = spacy.load("es_core_news_sm")
respuestas_simples = {"contacto": "Puedes contactarnos al teléfono (844)288-38-00 ☎️",}
palabras_clave = ["hola", "servicios", "escolares", "donde", "esta"]

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

# Función para calcular la similitud TF-IDF
def calculate_tfidf_similarity(pregunta, textos):
    vectorizer = TfidfVectorizer().fit_transform([pregunta] + textos)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:11]).flatten()
    print(f"Similares: {cosine_similarities}")
    return cosine_similarities

# Función para generar la consulta de la base de datos con palabras clave y entidades
def create_query(palabras_clave, entities):
    query = Q()
    all_keywords = palabras_clave + entities
    for palabra in all_keywords:
        query |= Q(titulo__icontains=palabra) | Q(informacion__icontains=palabra)
    return query

# Función para extraer las entidades nombradas de la pregunta
def extract_entities(pregunta):
    doc = nlp(pregunta)
    entities = [ent.text for ent in doc.ents]
    print(f"Entidades nombradas: {entities}")
    return entities

# Función para procesar la pregunta, eliminando stopwords y lematizando
def process_question(pregunta):
    pregunta_normalizada = pregunta.lower().strip()
    doc = nlp(pregunta_normalizada)
    palabras_clave_personalizadas = {"que", "donde", "quien", "año", "años", "hola"}
    tokens = [
        token.lemma_ for token in doc 
        if (not token.is_stop and token.is_alpha) or token.text in palabras_clave_personalizadas
    ]
    pregunta_procesada = " ".join(tokens) if tokens else pregunta_normalizada
    print(f"Pregunta procesada: {pregunta_procesada}")
    return pregunta_procesada


# Función para calcular la puntuación de cada resultado
def score_result(result, palabras_clave, entities, pregunta_procesada):
    score = 0
    texto_completo = f"{result.titulo.lower()} {result.informacion.lower()}"

    # Asignar puntuaciones a palabras clave y entidades
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

# Función para filtrar los resultados de la base de datos
def filter_results(pregunta):
    palabras_clave = process_question(pregunta)
    entities = extract_entities(pregunta)
    query = create_query(palabras_clave, entities)
    results = Database.objects.filter(query)[:100]  # Limitar resultados para rendimiento
    scored_results = [(result, score_result(result, palabras_clave, entities, process_question(pregunta))) for result in results]
    sorted_results = sorted(scored_results, key=lambda x: x[1], reverse=True)
    
    return sorted_results

# Función principal del chatbot
def chatbot(request):
    if request.method == 'POST':
        try:
            # Obtener y normalizar la pregunta
            data = json.loads(request.body)
            question = data.get('question', '').strip()

            if not question:
                return JsonResponse({'success': False, 'message': 'No puedo responder una pregunta que no existe 🤔🧐😬.'})

            # Verificar si la pregunta tiene una respuesta predefinida
            respuesta_simple = next((respuesta for clave, respuesta in respuestas_simples.items() if clave in question.lower()), None)
            if respuesta_simple:
                return JsonResponse({'success': True, 'answer': {'informacion': respuesta_simple}})

            # Procesar la pregunta y extraer entidades y palabras clave
            pregunta_procesada = process_question(question)
            entidades = extract_entities(question)
            palabras_clave = pregunta_procesada.split()
            
            # Crear la consulta a la base de datos usando las palabras clave y entidades
            query = create_query(palabras_clave, entidades)

            # Limitar la cantidad de resultados obtenidos de la base de datos para mejorar el rendimiento
            coincidencias = Database.objects.filter(query)[:100]  # Limitar a los primeros 100 resultados
            
            if not coincidencias:
                respuesta_default = {
                    "informacion": "Lo siento, no encontré información relacionada con lo que me pides 🤔. Puedes buscar más información en la página de preguntas frecuentes o, si gustas, también puedes enviarnos tus dudas. 😊😁",
                    "redirigir": "preguntas_frecuentes/",
                    "blank": False,
                }
                return JsonResponse({'success': True, 'answer': respuesta_default})

            # Buscar la mejor coincidencia
            mejor_coincidencia = None
            mejor_puntuacion = -1

            for coincidencia in coincidencias:
                puntuacion = score_result(coincidencia, palabras_clave, entidades, pregunta_procesada)
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_coincidencia = coincidencia

            # Si hay una coincidencia en la base de datos con buena puntuación
            if mejor_coincidencia:
                respuesta = {
                    "titulo": mejor_coincidencia.titulo,
                    "informacion": mejor_coincidencia.informacion,  # Usar la información directamente
                    "redirigir": mejor_coincidencia.redirigir,
                    "blank": True,
                    "imagenes": mejor_coincidencia.imagen.url if mejor_coincidencia.imagen else None
                }
                print(f"Respuesta: {respuesta, question}")
                return JsonResponse({'success': True, 'answer': respuesta})
            else:
                # Respuesta por defecto si no se encontró una coincidencia relevante
                respuesta_default = {
                    "informacion": "Lo siento, no encontré información relacionada con lo que me pides 🤔. Puedes buscar más información en la página de preguntas frecuentes o, si gustas, también puedes enviarnos tus dudas. 😊😁",
                    "redirigir": "preguntas_frecuentes/",
                    "blank": False,
                }
                return JsonResponse({'success': True, 'answer': respuesta_default})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Ocurrió un error al procesar el JSON. Código #400'})
        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Error en la clave del JSON: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})
