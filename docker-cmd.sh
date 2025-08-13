#!/bin/sh

echo "Start Gunicorn"
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3
