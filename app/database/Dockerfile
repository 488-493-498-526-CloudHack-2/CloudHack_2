# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "database_consumer.py"]