FROM python:3.13-slim

ARG DEPENDENCIES="vim nano build-essential libpq-dev gcc musl-dev postgresql-client"
RUN apt-get update && apt-get install -y $DEPENDENCIES

WORKDIR /opt/app

COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

VOLUME /media/
VOLUME /static/
EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "project.wsgi:application", "--workers=4", "--bind", "0.0.0.0:8000"]