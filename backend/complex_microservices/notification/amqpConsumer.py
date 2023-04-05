import pika
import json
from invokes import invoke_http
import amqp_setup

notification_URL = "http://localhost:5001/"


def callback(ch, method, properties, body):
    print("\nCALLBACK>>>>>>> \n" + __file__)
    print(json.loads(body))
    result = json.loads(body)
    print() # print a new line feed
#     # can call the next function to publish to another queue
    # Call the Flask app here
    # For example, you can use the requests library to make an HTTP request to a Flask endpoint
    notifAmqp_result = invoke_http(notification_URL, method='GET', json=result)
    print('notifAmqp_result:', notifAmqp_result)
    # return json.loads(notifAmqp_result)

amqp_setup.channel.basic_consume(queue='notification', on_message_callback=callback, auto_ack=True)

print('AMQP code waiting for messages...')
amqp_setup.channel.start_consuming()






# def queues():
#     amqp_setup.check_setup()     
#     queue_name = 'Subscription'
#     # set up a consumer and start to wait for coming messages
#     amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback_sub, auto_ack=True)
 
#     queue_name2 = 'ToBeneficiary'
#     # set up a consumer and start to wait for coming messages
#     amqp_setup.channel2.basic_consume(queue=queue_name2, on_message_callback=callback_ben, auto_ack=True)
    
#     queue_name3 = 'ToCompany'
#     # set up a consumer and start to wait for coming messages
#     amqp_setup.channel2.basic_consume(queue=queue_name3, on_message_callback=callback_comp, auto_ack=True)
    
#     queue_name4 = 'Cancel'
#     # set up a consumer and start to wait for coming messages
#     amqp_setup.channel2.basic_consume(queue=queue_name4, on_message_callback=callback_cancel, auto_ack=True)
    
#     #####################
    
#     amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
#     amqp_setup.channel2.start_consuming() # an implicit loop waiting to receive messages; 
#     amqp_setup.channel3.start_consuming() # an implicit loop waiting to receive messages; 
#     amqp_setup.channel4.start_consuming() # an implicit loop waiting to receive messages; 
    
    
# def callback_sub(channel, method, properties, body): # required signature for the callback; no return
#     print("\nCALLBACK SUB >>>>>>> \n" + __file__)
#     print(json.loads(body))
#     print() # print a new line feed
#     # can call the next function to publish to another queue
#     ############ This is for mass sending to all subscribers ## FROM listing_manage ##########
#     #Already has listing details + CompanyId
#     #needs to get userEmail + CompanyName
    

# def callback_ben(channel, method, properties, body): # required signature for the callback; no return
#     print("\nCALLBACK BEN >>>>>>> \n" + __file__)
#     print(json.loads(body))
#     print() # print a new line feed
#     # can call the next function to publish to another queue
#     ############ This is for a specific beneficiary ## FROM trans_manage ##########
#     #Already has transaction details + CompanyId + BeneficiaryId + listingId + listing details
#     #needs to get specific userEmail + specific CompanyName
    
# def callback_comp(channel, method, properties, body): # required signature for the callback; no return
#     print("\nCALLBACK COMP >>>>>>> \n" + __file__)
#     print(json.loads(body))
#     print() # print a new line feed
#     # can call the next function to publish to another queue
#     ############ This is for a specific company (successfulposting) ## FROM listing_manage ##########
#     #Already has listing details + CompanyId
#     #needs to get specificCompanyEmail + CompanyName
    
# def callback_cancel(channel, method, properties, body): # required signature for the callback; no return
#     print("\nCALLBACK CANCEL >>>>>>> \n" + __file__)
#     print(json.loads(body))
#     print() # print a new line feed
#     # can call the next function to publish to another queue
#     ############ This is for mass sending cancellation to involved users ## FROM trans_manage ##########
#     #i THINK i want listingID from ___ (anyth) (then can get all transactions involved from trans simple ms directly)
#     #needs transaction objs, then hv a list of beneficiaryID
#     #needs to get userEmails + CompanyName

