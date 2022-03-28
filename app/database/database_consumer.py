# Use this file to setup the database consumer that stores the ride information in the database
import psycopg2
import pika
import time
import requests
import os
import json


import psycopg2
pswd=os.getenv('POSTGRESPSWD')
db = os.getenv("HOST")
con = psycopg2.connect(user='postgres',
                       password=pswd, host=db)
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cc")
    cur.execute("CREATE TABLE cc(pickup VARCHAR(100),destination VARCHAR(100), time INT,cost REAL,seats INT)")
    print("table created")

#ch: channel,paramaters that come along with pika consumers
def callback(ch, method, properties, body): #put entry into database
    cmd = body.decode()
    cmd = json.loads(cmd)
    pick = cmd["pickup"]
    dest = cmd["destination"]
    t = cmd["time"]
    seats = cmd["seats"]
    cost = cmd["cost"]
    with con:
        cur.execute(f"INSERT INTO cc(pickup,destination,time,cost,seats) VALUES(\'{pick}\',\'{dest}\',\'{t}\',\'{cost}\',\'{seats}\')")
        print("Inserted")
        cur.execute(f"SELECT * FROM cc")	
        res = cur.fetchall()
        print(res)
    ch.basic_ack(delivery_tag=method.delivery_tag) #message has been consumer, del_tag:

while 1:
    sleepTime = 5
    print(' [*] Sleeping for ', sleepTime, ' seconds.')
    time.sleep(sleepTime)

    try:
        print(' [*] Connecting to server ...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='database', durable=True)

        print(' [*] Waiting for messages.')

        channel.basic_qos(prefetch_count=1) #qos:maximum number of messages on the queue, prefetch=true,shared across allconsumers on the channel
        channel.basic_consume(queue='database', on_message_callback=callback)
        channel.start_consuming()

    except Exception as e:
        print(e)