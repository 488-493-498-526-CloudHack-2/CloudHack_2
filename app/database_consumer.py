# Use this file to setup the database consumer that stores the ride information in the database
import psycopg2
import pika
import time
import requests
import os
import json


sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(sleepTime)

'''
@app.before_request
def create_connection():
	try:
		designation = request.args.get('designation')
		if 'db' not in g:
			g.db = psycopg2.connect(dbname="hd", user=designation, password="1234",host="127.0.0.1")
	except (Exception, psycopg2.Error) as error:
		print("Could not create connection:", error)

'''

import psycopg2
pswd=os.getenv('POSTGRESPSWD')
con = psycopg2.connect(database='test', user='postgres',
                       password=pswd, host=os.getenv('HOST'))
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cc")

    cur.execute("CREATE TABLE cc(pickup VARCHAR(100),destination VARCHAR(100), time INT,cost REAL,seats INT)")
    print("table created")

#ch: channel,paramaters that come along with pika consumers
def callback(ch, method, properties, body): #put entry into database
    cmd = body.decode()
    cmd = json.loads(cmd)
    #slpTime = cmd["time"]
    #print("[*] Ride for ",slpTime,"seconds")
    #time.sleep(slpTime)
    #print(" [x] Ride completed")
    pick = cmd["pickup"]
    dest = cmd["destination"]
    t = cmd["time"]
    seats = cmd["seats"]
    cost = cmd["cost"]
    with con:
        cur.execute(f"INSERT INTO cc(pickup,destination,time,cost,seats) VALUES(\'{pick}\',\'{dest}\',\'{t}\',\'{cost}\',\'{seats}\')")
    ch.basic_ack(delivery_tag=method.delivery_tag) #message has been consumer, del_tag:

    
try:
    #SERVER_IP = os.getenv("PRODUCER_ADDRESS")
    #CONSUMER_ID = os.getenv("CONSUMER_ID")
    #data = {"consumer_id":CONSUMER_ID, "name":CONSUMER_ID}
    #res = requests.post(SERVER_IP+"/new_ride_matching_consumer", json=data)
    #if not res.ok:
        #raise Exception("Response not received!!")
    
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