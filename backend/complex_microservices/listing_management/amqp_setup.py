
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from os import environ

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



import pika
import json
from invokes import invoke_http

notification_URL = "http://localhost:5001/"

# These module-level variables are initialized whenever a new instance of python interpreter imports the module;
# In each instance of python interpreter (i.e., a program run), the same module is only imported once (guaranteed by the interpreter).

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
))
    # Note about AMQP connection: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls.
    # If see: Stream connection lost: ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None)
    # - Try: simply re-run the program or refresh the page.
    # For rare cases, it's incompatibility between RabbitMQ and the machine running it,
    # - Use the Docker version of RabbitMQ instead: https://www.rabbitmq.com/download.html
        

channel = connection.channel()
# channel2 = connection.channel()
# channel3 = connection.channel()
# channel4 = connection.channel()

# Set up the exchange if the exchange doesn't exist
# - use a 'topic' exchange to enable interaction
exchangename="Notification_topic"
exchangetype="fanout"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)
    # 'durable' makes the exchange survive broker restarts

# Here can be a place to set up all queues needed by the microservices,
# - instead of setting up the queues using RabbitMQ UI.

############   notification queue   #############
#delcare notification queue
queue_name = 'notification'
channel.queue_declare(queue=queue_name, durable=True) 
    # 'durable' makes the queue survive broker restarts

#bind Subscription queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.notif') 
    # bind the queue to the exchange via the key
    # any routing_key ending with '.notif' will be matched

print(" amqp_setup.py: Done declaring and binding queues")




# ############   Cancel queue   #############
# #delcare Cancel queue
# queue_name = 'Cancel'
# channel.queue_declare(queue=queue_name, durable=True) 
#     # 'durable' makes the queue survive broker restarts

# #bind Subscription queue
# channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.cancel') 
#     # bind the queue to the exchange via the key
#     # any routing_key ending with '.cancel' will be matched


# ############   Subscription queue   #############
# #delcare Subscription queue
# queue_name = 'Subscription'
# channel.queue_declare(queue=queue_name, durable=True) 
#     # 'durable' makes the queue survive broker restarts

# #bind Subscription queue
# channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.subscribers') 
#     # bind the queue to the exchange via the key
#     # any routing_key ending with '.subscribers' will be matched

# ############   Company queue   #############
# #delcare company queue
# queue_name = 'ToCompany'
# channel.queue_declare(queue=queue_name, durable=True) 
#     # 'durable' makes the queue survive broker restarts

# #bind Subscription queue
# channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.company') 
#     # bind the queue to the exchange via the key
#     # any routing_key ending with '.subscribers' will be matched
    
# ############   Beneficiary queue   #############
# #delcare ToBeneficiary queue
# queue_name = 'ToBeneficiary'
# channel.queue_declare(queue=queue_name, durable=True) 
#     # 'durable' makes the queue survive broker restarts

# #bind ToBeneficiary queue
# channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='#.beneficiary') 
#     # bind the queue to the exchange via the key
#     # any routing_key ending with '.subscribers' will be matched

    

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    # The shared connection and channel created when the module is imported may be expired, 
    # timed out, disconnected by the broker or a client;
    # - re-establish the connection/channel is they have been closed
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    # For a BlockingConnection in AMQP clients,
    # when an exception happens when an action is performed,
    # it likely indicates a broken connection.
    # So, the code below actively calls a method in the 'connection' to check if an exception happens
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
