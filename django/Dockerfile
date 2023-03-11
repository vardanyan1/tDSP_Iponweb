FROM python:3

RUN apt-get update && apt-get install -y netcat


## Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1

## Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["/code/entrypoint.sh"]