FROM python:3.13.0a3-alpine

RUN apk update && apk add netcat-openbsd libjpeg-turbo-dev zlib-dev libpq

## Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1

## Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /code/

# Install packages using Pipenv
RUN pipenv install --system --deploy

# Copy the rest of the application code
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
