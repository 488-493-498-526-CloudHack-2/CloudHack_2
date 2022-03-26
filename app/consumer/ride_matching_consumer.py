import pika
import time
import requests
import os
import json

sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(sleepTime)

def callback(ch, method, properties, body):
    cmd = body.decode()
    cmd = json.loads(cmd)
    slpTime = cmd["time"]
    print("[*] Ride for ",slpTime,"seconds")
    time.sleep(slpTime)
    print(" [x] Ride completed")
    ch.basic_ack(delivery_tag=method.delivery_tag)

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
    channel.queue_declare(queue='new_ride', durable=True)

    print(' [*] Waiting for messages.')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='new_ride', on_message_callback=callback)
    channel.start_consuming()

except Exception as e:
    print(e)