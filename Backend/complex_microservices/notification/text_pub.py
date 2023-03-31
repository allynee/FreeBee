import json

import pika
import amqp_setup


# connection_parameters = pika.ConnectionParameters('localhost')
# connection = pika.BlockingConnection(connection_parameters)
# channel = connection.channel()
# channel.queue_declare(queue='letterbox')

############   Pub to Subscription queue (.subscribers) (meant to go directly to Notif MS)  #############
# obj = {'CompanyName': "Salvation Army" ,
#        'Subscribers': [{"email" : "lixuen.low.2021@scis.smu.edu.sg"}, {"email" : "llx16702@gmail.com"}]
#        }
# message = json.dumps(obj)
# amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="test.subscribers", 
#     body=message, properties=pika.BasicProperties(delivery_mode = 2))

# print(f"sending message: {message} to queue 'Subscription'")

# amqp_setup.connection.close()

############   Pub to Collection queue   #############
obj = {'ListingID': "924028319" ,
       'CorporateID': "3333"}
# message = json.dumps(obj)
# channel.basic_publish(exchange='', routing_key='letterbox', body=message)

message = json.dumps(obj)
amqp_setup.channel.basic_publish(exchange="Notification_topic", routing_key="test.notif", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2))

print(f"sending message: {message} to queue 'notification'")

#### TESTED, can receive >1 message in amqpConsumer ####

############   Pub to Collection queue   #############

# obj2 = {'ListingID': "1111111111" ,
#        'CorporateID': "3333"}

# message = json.dumps(obj2)
# amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="test.cancel", 
#     body=message, properties=pika.BasicProperties(delivery_mode = 2))

# print(f"sending message: {message} to queue 'Cancel'")
