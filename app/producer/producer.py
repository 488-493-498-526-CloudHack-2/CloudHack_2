# Code for Producer
from flask import Flask
from flask import request
import json
import pika

app = Flask(__name__)
consumer_data = []


@app.route('/new_ride',methods=["POST"])
def new_ride():
    my_new_string_value = request.data.decode("utf-8")
    data = json.loads(my_new_string_value)

    json_data = json.dumps(data)

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='new_ride',durable=True)
    channel.basic_publish(exchange='',
                        routing_key='new_ride',
                        body=json_data)
    print(" [x] Sent %r" % json_data)
    connection.close()

    return "Got data"

@app.route("/new_ride_matching_consumer",methods=["POST"])
def new_ride_matching_consumer():
    data = request.json

    consumer_id = data['consumer_id']
    name = data['name']
    ip = request.remote_addr
    req_ip = request.remote_addr

    mapp = dict()
    mapp[name,ip] = [consumer_id,req_ip]
    consumer_data.append(mapp)
    json_data = json.dumps(str(consumer_data))

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='new_ride_mat_con',durable=True)
    channel.basic_publish(exchange='',
                        routing_key='new_ride_mat_con',
                        body=json_data)
    print(" [x] Sent %r" % json_data)
    connection.close()
    return "Got data"

# @app.route("/")
# def home():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#     channel = connection.channel()
#     channel.queue_declare(queue='hello',durable=True)
#     channel.basic_publish(exchange='',
#                         routing_key='hello',
#                         body='Hello World!')
#     connection.close()
#     return "[x] Sent 'Hello World!'"

if __name__ == '__main__':
   app.run(debug = True)