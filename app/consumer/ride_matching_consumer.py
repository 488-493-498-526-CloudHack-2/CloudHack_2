import pika
import time
import requests
import os
import json

def callback(ch, method, properties, body):
    cmd = body.decode()
    cmd = json.loads(cmd)
    slpTime = cmd["time"]
    print("[*] Riding for ",slpTime,"seconds")
    time.sleep(slpTime)
    print(" [x] Ride completed")
    ch.basic_ack(delivery_tag=method.delivery_tag)

while 1:
    sleepTime = 5
    print(' [*] Sleeping for ', sleepTime, ' seconds.')
    time.sleep(sleepTime)
    try:
        SERVER_IP = os.getenv("PRODUCER_ADDRESS")
        CONSUMER_ID = os.getenv("CONSUMER_ID")
        data = {"consumer_id":CONSUMER_ID, "name":CONSUMER_ID}
        res = requests.post(SERVER_IP+"/new_ride_matching_consumer", json=data)
        if not res.ok:
            raise Exception("Response not received!!")
        
        print(' [*] Connecting to server ...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='ride_matching', durable=True)

        print(' [*] Waiting for messages.')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='ride_matching', on_message_callback=callback)
        channel.start_consuming()

    except Exception as e:
        print(e)