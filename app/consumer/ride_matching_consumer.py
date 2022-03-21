import pika
import time
import sys
sys.stdout.flush()


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    cmd = body.decode()
    with open("myfile.txt", "w") as file1:
    # Writing data to a file
        file1.write(cmd)

    if cmd == 'hey':
        print("hey there")
    elif cmd == 'hello':
        print("well hello there")
    else:
        print("sorry i did not understand ", body)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

while(True):
    try:
        # sleepTime = 10
        print(' [*] Sleeping for ', "5", ' seconds.')
        time.sleep(5)
    
        print(' [*] Connecting to server ...')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='hello', durable=True)
    
        print(' [*] Waiting for messages.')
    
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='hello', on_message_callback=callback)
        channel.start_consuming()
    
    except:
        print("errorrrrrrrrrrrr")