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

############   Pub For Subscription   #############
# obj = {
#   "purpose": "subscription",
#   "other_options": [
#     "toBeneficiary",
#     "toCorporate",
#     "cancel"
#   ],
#   "listing_result": {
#     "corporate_id": 123,
#     "corporate_name": "Salvation Barney",
#     "name": "string",
#     "description": "string",
#     "collection_details": "string",
#     "address": "Pasir Ris Street 21, Block 230, Singapore",
#     "postal": 510230,
#     "district": 18,
#     "area": "Pasir Ris Street 21, Block 230, Singapore",
#     "category": "string",
#     "quantity": 0,
#     "status": "string",
#     "listing_id": 19,
#     "created": "2023-03-31T10:20:02",
#     "modified": None
#   }
# }
# # message = json.dumps(obj)
# # channel.basic_publish(exchange='', routing_key='letterbox', body=message)

# message = json.dumps(obj)
# amqp_setup.channel.basic_publish(exchange="Notification_topic", routing_key="test.notif", 
#     body=message, properties=pika.BasicProperties(delivery_mode = 2))

# print(f"sending message: {message} to queue 'notification'")

#### TESTED, can receive >1 message in amqpConsumer ####



############   Pub To Inform Beneficiaries   #############
# obj2 = {
#   "purpose": "toBeneficiary",
#   "other_options": [
#     "subscription",
#     "toCorporate",
#     "cancel"
#   ],
#   "listing_result": {
#     "corporate_id": 0,
#     "corporate_name": "string",
#     "name": "string",
#     "description": "string",
#     "collection_details": "string",
#     "address": "Pasir Ris Street 21, Block 230, Singapore",
#     "postal": 510230,
#     "district": 18,
#     "area": "Pasir Ris Street 21, Block 230, Singapore",
#     "category": "string",
#     "quantity": 0,
#     "status": "string",
#     "listing_id": 19,
#     "created": "2023-03-31T10:20:02",
#     "modified": None
#   },
#   "transaction_result": {
#     "transaction_id": 0,
#     "listing_id": 19,
#     "beneficiary_id": 123,
#     "corporate_id": 123,
#     "status": "Cancelled",
#     "quantity": 0
#   }
# }
# # In Progress
# # 2) Ready for Collection 
# # 3) Completed
# # 4) Cancelled
# # message = json.dumps(obj)
# # channel.basic_publish(exchange='', routing_key='letterbox', body=message)

# message = json.dumps(obj2)
# amqp_setup.channel.basic_publish(exchange="Notification_topic", routing_key="test.notif", 
#     body=message, properties=pika.BasicProperties(delivery_mode = 2))

# print(f"sending message: {message} to queue 'notification'")

# #### TESTED, can receive >1 message in amqpConsumer ####


###########   Pub successful posting of listing to corporate   #############
# obj3 = {
#   "purpose": "toCorporate",
#   "other_options": [
#     "toBeneficiary",
#     "subscription",
#     "cancel"
#   ],
#   "listing_result": {
#     "corporate_id": "6ubkEQJU3ZaQ8NM1vdqQQowGMQJ3",
#     "corporate_name": "Salvation Barney",
#     "name": "string",
#     "description": "string",
#     "collection_details": "string",
#     "address": "Pasir Ris Street 21, Block 230, Singapore",
#     "postal": 510230,
#     "district": 18,
#     "area": "Pasir Ris Street 21, Block 230, Singapore",
#     "category": "string",
#     "quantity": 0,
#     "status": "string",
#     "listing_id": 19,
#     "created": "2023-03-31T10:20:02",
#     "modified": None
#   }
# }
# # message = json.dumps(obj)
# # channel.basic_publish(exchange='', routing_key='letterbox', body=message)

# message = json.dumps(obj3)
# amqp_setup.channel.basic_publish(exchange="Notification_topic", routing_key="test.notif", 
#     body=message, properties=pika.BasicProperties(delivery_mode = 2))

# print(f"sending message: {message} to queue 'notification'")

#### TESTED, can receive >1 message in amqpConsumer ####

###########   Cancellation   #############
obj4 = {
  "purpose": "cancelled",
  "other_options": [
    "toBeneficiary",
    "subscription",
    "toCorporate"
  ],
  "listing_result": {
    "corporate_id": "6ubkEQJU3ZaQ8NM1vdqQQowGMQJ3",
    "corporate_name": "Salvation Barney",
    "name": "string",
    "description": "string",
    "collection_details": "string",
    "address": "Pasir Ris Street 21, Block 230, Singapore",
    "postal": 510230,
    "district": 18,
    "area": "Pasir Ris Street 21, Block 230, Singapore",
    "category": "string",
    "quantity": 0,
    "status": "string",
    "listing_id": "-NS066ADh061Or7ifciC",
    "created": "2023-03-31T10:20:02",
    "modified": None
  }
}
# message = json.dumps(obj)
# channel.basic_publish(exchange='', routing_key='letterbox', body=message)

message = json.dumps(obj4)
amqp_setup.channel.basic_publish(exchange="Notification_topic", routing_key="test.notif", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2))

print(f"sending message: {message} to queue 'notification'")

#### TESTED, can receive >1 message in amqpConsumer ####