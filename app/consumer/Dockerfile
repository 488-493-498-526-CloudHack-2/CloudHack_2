FROM python:latest

WORKDIR /consumer

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "ride_matching_consumer.py"]