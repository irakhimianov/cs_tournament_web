import os
from pathlib import Path

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', '_')

DEBUG = bool(int(os.getenv('DEBUG', 1)))

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = []

CORS_ORIGIN_WHITELIST = []

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_standardized_errors',
    'drf_spectacular',
    'django_filters',

    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
    'league.apps.LeagueConfig',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('SQL_DATABASE', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('SQL_USER', 'user'),
        'PASSWORD': os.getenv('SQL_PASSWORD', 'password'),
        'HOST': os.getenv('SQL_HOST', 'localhost'),
        'PORT': int(os.getenv('SQL_PORT', 5432)),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

LANGUAGES = [
    ('ru', _('Русский')),
    ('en', _('English')),
]

TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Moscow')

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

REDIS_DB = int(os.getenv('REDIS_DB', 1))

CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 10))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        'TIMEOUT': CACHE_TIMEOUT,
    },
}

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Template')

PROJECT_URL = os.getenv('PROJECT_URL', 'http://127.0.0.1:8000/')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S%Z',
    'DATETIME_INPUT_FORMAT': '%Y-%m-%d %H:%M:%S%Z',
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.ApiPagination',
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}

SPECTACULAR_SETTINGS = {
    'TITLE': PROJECT_NAME,
    'SERVE_INCLUDE_SCHEMA': False,
    'SORT_OPERATION_PARAMETERS': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]+/',
}

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

CELERY_TIMEZONE = TIME_ZONE

try:
    from project.local_settings import *
except ImportError:
    print("Warning: no local_settings.py")
