#!/usr/bin/env bash
set -e

if [ -n "POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
  until pg_isready -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-postgres}" >/dev/null 2>&1;
  do sleep 1
  done
fi

echo "Apply migrations"
python manage.py migrate --noinput

echo "Apply fixtures"
python manage.py loaddata auth.json

echo "Collect static"
python manage.py collectstatic --noinput

exec "$@"
