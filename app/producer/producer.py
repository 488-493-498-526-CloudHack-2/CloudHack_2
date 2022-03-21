# Code for Producer
from flask import Flask
from flask import request
import json
import pika
import time

time.sleep(15)

app = Flask(__name__)
consumer_data = []


@app.route('/new_ride',methods=["POST"])
def new_ride():
    my_new_string_value = request.data.decode("utf-8")
    data = json.loads(my_new_string_value)
    pickup = data['pickup']
    destination = data['destination']
    time = data['time']
    cost = data['cost']
    seats = data['seats']
    return "Got data"

@app.route("/new_ride_matching_consumer",methods=["POST"])
def new_ride_matching_consumer():
    my_new_string_value = request.data.decode("utf-8")
    data = json.loads(my_new_string_value)
    consumer_id = data['consumer_id']
    ip = data['ip']
    req_ip = data['req_ip']
    name = data['name']
    mapp = dict()
    mapp[name,ip] = [consumer_id,req_ip]
    consumer_data.append(mapp)
    return "Got data"

@app.route("/")
def home():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='hello',durable=True)
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='Hello World!')
    connection.close()
    return "[x] Sent 'Hello World!'"

@app.teardown_appcontext
def teardown_rabbitmq(exception):
    print("app destoryed")


if __name__ == '__main__':
   app.run(debug = True)