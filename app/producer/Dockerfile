# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP producer.py

CMD ["flask", "run", "--host=0.0.0.0"]