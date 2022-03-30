# Code for Producer
from flask import Flask
from flask import request
import json
import pika
import time

app = Flask(__name__)
consumer_data = []
mapp = dict()

global connection, channel

while 1:
    try:
        time.sleep(5)
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='ride_matching',durable=True)
        channel.queue_declare(queue='database',durable=True)
        break
    except Exception as e:
        print(e)

@app.route('/new_ride',methods=["POST"])
def new_ride():
    my_new_string_value = request.data.decode("utf-8")
    data = json.loads(my_new_string_value)

    json_data = json.dumps(data)

    channel.basic_publish(exchange='',
                        routing_key='ride_matching',
                        body=json_data)
    print(" [x] Sent %r to ride_matching queue" % json_data)

    channel.basic_publish(exchange='',
                        routing_key='database',
                        body=json_data) #exchange receives messages from producer amd pushes it to queues, nameless exchange 
    print(" [x] Sent %r to database queue" % json_data)

    return "Pushed to queues"

@app.route("/new_ride_matching_consumer",methods=["POST"])
def new_ride_matching_consumer():
    data = request.json
    consumer_id = data['consumer_id']
    name = data['name']
    ip = request.remote_addr #get consumer's ip address??
    req_ip = request.remote_addr 

    mapp[name,ip] = [consumer_id,req_ip]
    consumer_data.append(mapp)
    return " [x] Array contains %r" % consumer_data

if __name__ == '__main__':
   app.run(debug = True)