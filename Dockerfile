FROM python:3.9-slim-buster

WORKDIR /code

ENV PYTHONUNBUFFERED=1 

ENV PYTHONPATH /code

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql python-psycopg2 libpq-dev \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code/
