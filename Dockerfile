FROM python:3.13-slim as base

ARG DEPENDENCIES="vim nano build-essential libpq-dev gcc musl-dev postgresql-client"
RUN apt-get update && apt-get install -y $DEPENDENCIES

WORKDIR /opt/app

COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base

RUN chmod +x ./docker-entrypoint.sh && chmod +x ./docker-cmd.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/docker-cmd.sh"]