"""
Django settings for cross_project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import environ
import dj_database_url
from pathlib import Path

env = environ.Env()
environ.Env.read_env()
OPENAI_API_KEY = env('OPENAI_API_KEY')


BASE_DIR = Path(__file__).resolve().parent.parent

# Cambiar la clave secreta en produccion ---------------------------------------------------------
SECRET_KEY = 'django-insecure-32wpj55%1@sy+hqt(v6b87!04o3m2(+1##sf@^%45$0@@fdynj'

# Camibiar debug en produccion IMPORTANTE ---------------------------------------------------------
DEBUG = True

ALLOWED_HOSTS = []

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# Base de datos, utilizar PostgreSQL de preferencia -------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://cross_asistent_production_user:3zBDxS8OZ66dvPGsXZ0leTTk1X4o129B@dpg-cr40bbrtq21c73drq1k0-a.oregon-postgres.render.com/cross_asistent_production',
        conn_max_age=600
    )
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_URL = '/acceder'
LOGOUT_URL = '/acceder'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'