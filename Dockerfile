FROM python:3.13-slim AS base

ARG DEPENDENCIES="vim nano build-essential libpq-dev gcc musl-dev postgresql-client"
RUN apt-get update && apt-get install -y $DEPENDENCIES

WORKDIR /opt/app

COPY pyproject.toml poetry.lock ./
ARG POETRY_VERSION="2.1.1"
RUN pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root


FROM base AS dev
COPY . .
RUN poetry install --all-groups


FROM base AS prod
COPY . .

RUN python manage.py migrate --noinput && python manage.py loaddata auth.json && python manage.py collectstatic --noinput
CMD ["gunicorn", "project.wsgi:application", "--workers=4", "--bind", "0.0.0.0:8000"]