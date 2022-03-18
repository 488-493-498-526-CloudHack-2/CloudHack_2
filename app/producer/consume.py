import pika
def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)