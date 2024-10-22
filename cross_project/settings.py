import os
import environ
from pathlib import Path
from cryptography.fernet import Fernet

env = environ.Env()
environ.Env.read_env()

encryption_key = env("ENCRYPTION_KEY").encode()
fernet = Fernet(encryption_key)
encrypted_api_key = env("OPENAI_API_KEY").encode()
decrypted_api_key = fernet.decrypt(encrypted_api_key).decode()


OPENAI_API_KEY = decrypted_api_key

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE_PATH = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_FILE_PATH):
    environ.Env.read_env(ENV_FILE_PATH)

# Cambiar la clave secreta en produccion ---------------------------------------------------------
SECRET_KEY = 'django-insecure-32wpj55%1@sy+hqt(v6b87!04o3m2(+1##sf@^%45$0@@fdynj'
DEBUG = True

ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['10.1.1.113']
#if DEBUG:
    #ALLOWED_HOSTS = ['10.1.1.113']
    #ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

INSTALLED_APPS = [
    'cross_asistent',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cross_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cross_project.wsgi.application'

# Base de datos local -------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#conect to MySQL ################
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'nombre_base_datos',
#        'USER': 'usuario',
#        'PASSWORD': 'contraseña',
#        'HOST': 'localhost',  # O la dirección IP del servidor
#        'PORT': '3306',  # Puerto por defecto de MySQL
#    }
#}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True


# Documentos estaticos ##########################
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# destruccion de la sesion #######################
LOGIN_URL = '/acceder/'
LOGOUT_URL = '/acceder/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'