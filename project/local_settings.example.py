# Пример заполнения local_settings.py, в котором отражаем то, что будет перезаписываться
# либо разработчиком в своей локальной среде, либо сценариями выкладки.

DEBUG = True

SECRET_KEY = 'SECRET_KEY'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['*']

CORS_ORIGIN_WHITELIST = ['*']

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
