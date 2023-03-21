
import pika

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='letterbox')

message = "lixuen.low.2021@scis.smu.edu.sg"

channel.basic_publish(exchange='', routing_key='letterbox', body=message)

print(f"sending message: {message} to queue 'letterbox'")

connection.close()

