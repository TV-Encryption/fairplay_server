# Fairplay Server

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/pydanny/cookiecutter-django/)

_Retrieves keys and provides them using Fairplay_

## Development Setup

First of all, you need to clone the `FairplayKSM` into the `docker`directory. Otherwise it will be missing the KSM.

Copy the `.env.example` file to `.env` and modify the secret values with your own

Also put the private key at `secrets/dev_private_key.pem`

You can create the Django secret key with:
```shell
docker run --rm django python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

On the first run, you have to initialize the database:
```shell
docker-compose up -d postgres
docker-compose run --rm --no-deps django python manage.py migrate
docker-compose run --rm --no-deps django python manage.py collectstatic
```

Then start your dev-env with `docker-compose up -d`

### Executing tests locally

You can either run the tests via PyCharm with the configured run-configurations or do them with docker-compose manually:

```shell
docker-compose run -e DJANGO_SETTINGS_MODULE=config.settings.test --rm django pytest
```

If the tests abort unexpectedly they won't run until the test database is removed. Either recreate the database or run the following command:

```shell
docker-compose run --rm django python manage.py drop_test_database
```

#### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

```shell
docker-compose run -e DJANGO_SETTINGS_MODULE=config.settings.test --rm django coverage run -m pytest
docker-compose run -e DJANGO_SETTINGS_MODULE=config.settings.test --rm django coverage html
open htmlcov/index.html
```

### Linting

The project is set up with [pre-commit](https://pre-commit.com/#install). For it to work, it needs to be outside docker.

To activate it for a project run:
```shell
pre-commit install
```

The next time you commit, it is going to lint and check your files. Sometimes you need to review the changes and do the commit again. If you want to commit without checks
```shell
git commit --no-verify
```

### Container explanation
- `celerybeat` The periodic task scheduler
- `celeryworker` The worker to execute Tasks (mainly importing new data)
- `flower` Task viewer for celery
- `django` The API
- `postgres` The DB
- `redis` Cache and Celery broker
- `mailhog` Test mailserver

### Django commands
List available commands:
```shell
docker-compose run --rm django python manage.py -h
```
All the commands contain a help (`-h/--help`).

### Setting Up Your Users

To create an **superuser account**, use this command:

```shell
docker-compose run --rm django python manage.py createsuperuser
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [`MailHog`](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``
