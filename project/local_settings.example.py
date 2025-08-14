# Пример заполнения local_settings.py, в котором отражаем то, что будет перезаписываться
# либо разработчиком в своей локальной среде, либо сценариями выкладки.
import os

DEBUG = True

SECRET_KEY = 'SECRET_KEY'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', []).split(',')

CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST', []).split(',')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
