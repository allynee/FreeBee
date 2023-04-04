
import json

import pika
import amqp_setup

import os

################   CONSUMING FROM COLLECTION QUEUE   ##################
monitorBindingKey='.collection'

def receiveNotifToGetSubs():
    amqp_setup.check_setup()
        
    queue_name = 'Collection'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

############   THIS PROCESSES IT INTO JSON AND CALLS THE PUB FUNCTION   #############
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    print(json.loads(body))
    print() # print a new line feed
    # can call the next function to publish to another queue
    pubToSubs(json.loads(body))

############   PUB TO SUBSCRIPTION QUEUE WHICH GOES TO NOTIF MS  #############
def pubToSubs(order):
    print("Publishing to Subscription queue:")
    print("Recieved: ")
    print(order)
    print("Will process it and send output to notif MS")
    ############### Pretend Im Processing Company ID to get this info #################
    obj = {'CompanyName': "Salvation Army" ,
           'Subscribers': [{"email" : "lixuen.low.2021@scis.smu.edu.sg"}, {"email" : "llx16702@gmail.com"}]
           }
    message = json.dumps(obj)
    ############### Pretend Im Processing Company ID to get this info #################
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="test.subscribers", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))

    print(f"sending message: {message} to queue 'Subscription'")

    
    
    # amqp_setup.connection.close()

# def processOrderLog(order):
#     print("Recording an order log:")
#     print(order)
    

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotifToGetSubs()