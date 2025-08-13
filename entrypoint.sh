#!/usr/bin/env bash
set -e

if [ -n "SQL_HOST" ]; then
  echo "Waiting for Postgres at ${SQL_HOST}:${SQL_PORT:-5432}..."
  until pg_isready -h "${SQL_HOST}" -p "${SQL_PORT:-5432}" -U "${SQL_USER:-postgres}" >/dev/null 2>&1;
  do sleep 1
  done
fi

echo "Apply migrations"
python manage.py migrate --noinput

echo "Apply fixtures"
python manage.py loaddata auth.json

echo "Collect static"
python manage.py collectstatic --noinput

echo "Start Gunicorn"
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3

exec "$@"
