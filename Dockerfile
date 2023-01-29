ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

RUN apt-get update -yq \
    && apt-get -yq install curl gnupg ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash \
    && apt-get update -yq \
    && apt-get install -yq \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-setuptools \
        python3-wheel \
        nodejs

RUN mkdir -p /app
WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

COPY . .

WORKDIR theme/static_src/
RUN npm install

WORKDIR /app

RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput


EXPOSE 8080

# replace APP_NAME with module name
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "tankobon.wsgi"]
