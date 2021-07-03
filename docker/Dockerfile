FROM python:3.8-buster AS builder
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install build-essential cmake cppcheck valgrind clang lldb llvm gdb \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libssl-dev

WORKDIR /app
COPY docker/FairplayKSM .
RUN cmake -B./build . && cmake --build ./build

FROM python:3.8-slim-buster AS base

ENV PYTHONUNBUFFERED 1
ENV USE_DOCKER yes

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Dependency for FairplayKSM
  && apt-get install -y openssl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

# Entrypoint
COPY ./docker/entrypoint /entrypoint
COPY ./docker/worker-entrypoint /worker-entrypoint
COPY ./docker/bin /usr/local/bin

COPY --from=builder /app/build/FairplayKSM.so /usr/local/lib/python3.8/site-packages/
COPY --from=builder /app/FairplayKSM.pyi /usr/local/lib/python3.8/site-packages/

### Dev Environment ###
### -------------------- ###
FROM base as dev
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements/dev.txt /requirements/
RUN pip install --no-cache-dir -r /requirements/dev.txt

RUN mkdir -p /app && chown django:django -R /app
WORKDIR /app
USER django:django
ENTRYPOINT ["/worker-entrypoint"]

### Application Image ###
### ----------------- ###
FROM base AS prod

ENV DJANGO_SETTINGS_MODULE config.settings.base

COPY --chown=django:django . /app/
WORKDIR /app
USER django:django

#### Django Prod
FROM prod AS prod-django

EXPOSE 5000
ENTRYPOINT ["/entrypoint"]
CMD ["start"]

#### Celery Worker Prod
FROM prod AS prod-worker
ENTRYPOINT ["/worker-entrypoint"]
CMD ["start-celeryworker"]

#### Celery Beat
FROM prod AS prod-beat
ENTRYPOINT ["/worker-entrypoint"]
CMD ["start-celerybeat"]
