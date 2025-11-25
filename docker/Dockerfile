FROM python:3.13.6-slim-bullseye AS base

ENV PYTHONUNBUFFERED=1
ENV APPLICATION_NAME=jabberwocky

WORKDIR /app/src

COPY ./requirements/base.txt ./requirements/production.txt /app/requirements/
RUN pip install --no-cache-dir --disable-pip-version-check \
    -r /app/requirements/production.txt

FROM base AS prod

COPY ./scripts /app/scripts
COPY ./docker/assets/gunicorn /var/gunicorn
COPY ./src /app/src

EXPOSE 8000

ENTRYPOINT ["/app/scripts/app-command.sh"]

FROM base AS dev

COPY ./requirements /app/requirements

RUN pip install --no-cache-dir --disable-pip-version-check \
    -r /app/requirements/production.txt \
    -r /app/requirements/test.txt \
    -r /app/requirements/linting.txt

WORKDIR /app/src
