import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)