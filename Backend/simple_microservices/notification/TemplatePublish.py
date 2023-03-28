
################   HOW TO USE AMQP   ################
# 1. docker run -d --hostname esd-rabbit --name rabbitmq-mgmt -p 5672:5672 -p 15672:15672 rabbitmq:3-management
#    (start the rabbitmq server on docker)
# 2. run amqp_setup.py
# 3. run the publisher code
# optional --> to see the successful consumption, need to run the consumer text


#################   SETUP IMPORTS   #################
#####################################################

import json

import pika
import amqp_setup

#################   QUEUE INDEX   #################
#####################################################
#### To Subscribers:
# Queue name ==> “Subscription”
# Routing Key ==> “email.subscribers” / "#.subscribers"
# 1. Notifying all Subscribers upon new listing ==> subscribers

#### To Multiple Users:
# Queue name ==> “Cancel”
# Routing Key ==> “email.company” / "#.cancel"
# 1. Company canceling listing that is up

#### To Specific Company:
# Queue name ==> “ToCompany”
# Routing Key ==> “email.company” / "#.company"
# 1. Listing quantity hits 0 
# 2. Confirmation that listing has been successfully posted 

#### To a Specific User:
# Queue name ==> “ToBeneficiary”
# Routing Key ==> “email.beneficiary” / "#.beneficiary"
# 1. Item is requested → transaction pending
# 2. Item is ready for collection → transaction ready for collection
# 3. Item has been collected! → transaction successful
# 4. Iw to cancel transaction → transaction canceled

############  EG - Pub to Cancel queue   #############
#####################################################
obj = {'ListingID': "2324" ,
       'CorporateID': "3333"}
# message = json.dumps(obj)
# channel.basic_publish(exchange='', routing_key='letterbox', body=message)

message = json.dumps(obj)
amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.cancel", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2))

print(f"sending message: {message} to queue 'collection'")

