#!/usr/bin/env bash
set -e

echo "Waiting for DB..."
python - <<'PY'
import time, sys
from django.db import connections
from django.db.utils import OperationalError
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Инициализируем Django (импортируем только когда настройки доступны)
import django
django.setup()

for i in range(60):
    try:
        connections['default'].cursor()
        print("DB is up!")
        sys.exit(0)
    except OperationalError:
        print("DB not ready, retrying...")
        time.sleep(1)
sys.exit(1)
PY

echo "Apply migrations"
python manage.py migrate --noinput

echo "Apply fixtures"
python manage.py loaddata auth.json

echo "Collect static"
python manage.py collectstatic --noinput

echo "Start Gunicorn"
exec gunicorn project.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-4} \
  --timeout ${GUNICORN_TIMEOUT:-120}
