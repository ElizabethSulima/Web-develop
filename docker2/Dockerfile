FROM python:3.9.13-slim-buster as builder

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
# RUN pip install --no-cache-dir -r requirements.txt 

COPY . /usr/src/app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
