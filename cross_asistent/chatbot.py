from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import Database
import unicodedata
import openai
import spacy
import json

# ChatBot ----------------------------------------------------------
# Cargar el modelo de lenguaje español
# analizar texto en aplicaciones de procesamiento de lenguaje natural.
nlp = spacy.load("es_core_news_sm")
# Diccionario de respuestas simples predefinidas
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

def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def process_question(pregunta):
    pregunta_normalizada = normalize_text(pregunta.lower().strip())

    doc = nlp(pregunta_normalizada)
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

def filter_results(pregunta):
    palabras_clave = process_question(pregunta)
    entities = extract_entities(pregunta)
    query = create_query(palabras_clave, entities)

    results = Q.objects.filter(query)
    scored_results = [(result, score_result(result, palabras_clave, entities, process_question(pregunta))) for result in results]
    sorted_results = sorted(scored_results, key=lambda x: x[1], reverse=True)

    return sorted_results

def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()

            if not question:
                return JsonResponse({'success': False, 'message': 'No puedo responder una pregunta que no existe 🤔🧐😬.'})

            respuesta_simple = next((respuesta for clave, respuesta in respuestas_simples.items() if clave in question), None)
            if respuesta_simple:
                return JsonResponse({'success': True, 'answer': {'informacion': respuesta_simple}})

            pregunta_procesada = process_question(question)
            entidades = extract_entities(question)
            palabras_clave = pregunta_procesada.split()
            query = create_query(palabras_clave, entidades)

            coincidencias = Database.objects.filter(query)
            mejor_coincidencia = None
            mejor_puntuacion = -1

            for coincidencia in coincidencias:
                puntuacion = score_result(coincidencia, palabras_clave, entidades, pregunta_procesada)
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_coincidencia = coincidencia

            if mejor_coincidencia:
                informacion = mejor_coincidencia.informacion
                system_prompt = f"Eres Hawky, un asistente de la Universidad Tecnologica de Coahuila. Utiliza alguno emojis sutilmente. Responde la pregunta con esta información pero tu no hagas preguntas: {informacion}"
                answer = chatgpt(question, system_prompt)

                respuesta = {
                    "titulo": mejor_coincidencia.titulo,
                    "informacion": answer,
                    "redirigir": mejor_coincidencia.redirigir,
                    "blank": True,
                    "imagenes": mejor_coincidencia.imagen.url if mejor_coincidencia.imagen else None
                }

                print(f"Respuesta {respuesta}")
                return JsonResponse({'success': True, 'answer': respuesta})

            respuesta_default = {
                "informacion": "Lo siento, no encontre informacion relacionada con lo que me pides 🤔. Puedes buscar mas informacion en la pagina de preguntas frecuentes o, si gustas, tambien puedes enviarnos tus dudas. 😊😁",
                "redirigir": "preguntas_frecuentes/",
                "blank": False,
            }
            return JsonResponse({'success': True, 'answer': respuesta_default})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Ocurrio un error, Al parecer no se permite este metodo. Codigo #400'})
        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Error en la clave del JSON: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

