from django.contrib.auth.models import User
from django.db import IntegrityError
import spacy

# ChatBot ---------------------------------------------------
# Cargar el modelo de lenguaje español
# analizar texto en aplicaciones de procesamiento de lenguaje natural.
nlp = spacy.load("es_core_news_sm")
# Diccionario de respuestas simples predefinidas
respuestas_simples = {
    "ubicacion": "Nos encontramos en la Av.Industria Metalúrgica #2001 Parque Industrial Ramos Arizpe Coahuila C.P.25900.",
    "contacto": "Puedes contactarnos al teléfono (844)288-38-00 ☎️",
}


# Mapa ---------------------------------------------------
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



# Crear nuevo usuario Funcion ---------------------------------------------
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


