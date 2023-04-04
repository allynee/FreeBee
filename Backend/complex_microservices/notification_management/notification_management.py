from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

from invokes import invoke_http

# import amqp_setup
import pika
import json
import amqp_setup

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
CORS(app)

listing_URL = environ.get('listing_URL') or "http://localhost:8000/listing"
transaction_URL = environ.get('transaction_URL') or "http://localhost:9000/transaction"
# geocoding_URL = "http://localhost:3000/"
# notification_URL = "http://localhost:5001/" #this is this page
# authentication_URL = "localhost:3001/"
notification_URL = environ.get('notification_URL') or "http://localhost:5005/sendmail"
user_URL = environ.get('user_URL') or "http://localhost:8421"


@app.route("/", methods=['GET'])
###################################################################
# def callConsumer():
#     amqp_setup.check_setup()
#     amqp_setup.channel.basic_consume(queue='notification', on_message_callback=callback, auto_ack=True)

#     print('AMQP code waiting for messages...')
#     amqp_setup.channel.start_consuming()

# def callback(ch, method, properties, body):
#     print("\nCALLBACK>>>>>>> \n" + __file__)
#     print(json.loads(body))
#     result = json.loads(body)
#     print() # print a new line feed
# #     # can call the next function to publish to another queue
#     # Call the Flask app here
#     # For example, you can use the requests library to make an HTTP request to a Flask endpoint
#     notifAmqp_result = invoke_http(notification_URL, method='GET', json=result)
#     print('notifAmqp_result:', notifAmqp_result)

###################################################################
def recieveMail():
    if request.is_json:
        try:
            info = request.get_json()
            print("<br>Received info in JSON:", info)        
         
            # do the actual work
            # 1. recieve info 
            result = sortMail(info)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "notification.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
###################################################################

def sortMail(info):
    #sort mail here
    if info['purpose'] == "subscription":
        subscription(info)
    elif info['purpose'] == "toBeneficiary":
        toBeneficiary(info)
    elif info['purpose'] == "toCorporate":
        print("toCorporate")
        toCorporate(info)
    elif info['purpose'] == "cancelled":
        cancel(info)

def subscription(info):
#     ############ This is for mass sending to all subscribers ## FROM listing_manage ##########
#     #Already has listing details + CompanyId
#     #needs to get userEmail + CompanyName
    print('<br>-----Invoking user microservice-----')
    corporate_id = info['listing_result']['corporate_id']
    print(corporate_id)
    full_user_URL = user_URL + f"/subscription/corporate/{corporate_id}"
    subscription_result = invoke_http(full_user_URL, method='GET', json=None)
    print('subscription_result:', subscription_result) #this returns a list of the beneficiary info
    corporate_name =info['listing_result']['corporate_name']
    if subscription_result != []:
        for sub in subscription_result:
            email = sub['email']
            username = sub['username']
            subject = f"{corporate_name} has posted a new listing!"
            message = f"Hi {username} aka {email}! <br><br>{corporate_name} has posted a new listing! <br>Please check it out at {listing_URL}{str(info['listing_result']['listing_id'])}<br><br>Thank you for using FreeBee!"
            sendEmail('lixuen.low.2021@scis.smu.edu.sg', subject, message);
    # doEmail();

def toBeneficiary(info):
#     ############ This is for a specific beneficiary ## FROM trans_manage ##########
#     #Already has transaction details + CompanyId + BeneficiaryId + listingId + listing details
#     #needs to get specific userEmail + specific CompanyName
    print('<br>-----Invoking user microservice-----')
    corporate_name = info['listing_result']['corporate_name']
    beneficiary_id = info['transaction_result']['beneficiary_id']
    status = info['transaction_result']['status'] #In Progress, Ready for Collection, Completed, Cancelled
    full_user_URL = user_URL + f"/beneficiary/{beneficiary_id}"
    beneficiary_result = invoke_http(full_user_URL, method='GET', json=None) #returns beneficiary details
    print('beneficiary_result:', beneficiary_result) #this returns a list of the beneficiary info
    email = beneficiary_result['email']
    username = beneficiary_result['username']
    if status == "In Progress":
        subject = f"Your claim is in progress!"
        message = f"Hi {username} aka {email}!<br><br>You have successfully claimed an item - {info['listing_result']['name']}!<br>Please may check the collection details in FreeBee and you'll be notified again when the item is ready for collection!<br><br>Thank you for using FreeBee!"
    if status == "Ready for Collection":
        subject = f"Your claim is ready for collection!"
        message = f"Hi {username} aka {email}!<br><br>Your item - {info['listing_result']['name']} is ready for collection!<br>The collection details are as follows:<br>{info['listing_result']['collection_details']}<br>Collect at: {info['listing_result']['address']}, {info['listing_result']['postal']}<br><br>Thank you for using FreeBee!"
    if status == "Completed":
        subject = f"Your item has been successfully collected!"
        message = f"Hi {username} aka {email}!<br><br>Your item - {info['listing_result']['name']} has been collected!<br><br>Thank you for using FreeBee!"
    # if status == "Cancelled":
    #     subject = f"Your item collection has been cancelled!"
    #     message = f"Hi {username} aka {email}!<br><br>Your item - {info['listing_result']['name']} has been cancelled by {corporate_name}!<br>We apologize for any inconvinience caused<br><br>Thank you for using FreeBee!"
    sendEmail('lixuen.low.2021@scis.smu.edu.sg', subject, message);
    # doEmail();


def toCorporate(info):
#     ############ This is for a specific company (successfulposting) ## FROM listing_manage ##########
#     #Already has listing details + CompanyId
#     #needs to get specificCompanyEmail + CompanyName
    print('<br>-----Invoking user microservice-----')
    corporate_id = info['listing_result']['corporate_id']
    print(corporate_id)
    full_user_URL = user_URL + f"/corporate/{corporate_id}"
    corporate_result = invoke_http(full_user_URL, method='GET', json=None)
    print('subscription_result:', corporate_result) #this returns coportate details
    corporate_name = info['listing_result']['corporate_name']
    email = corporate_result['email']
    subject = f"Successfully posted listing!"
    message = f"Hi {corporate_name} aka {email}! <br><br>You have successfully posted a new listing - {info['listing_result']['name']}! <br><br>Thank you for using FreeBee!"
    sendEmail('lixuen.low.2021@scis.smu.edu.sg', subject, message);


def cancel(info):
#     ############ This is for mass sending cancellation to involved users ## FROM trans_manage ##########
#     #i THINK i want listingID from ___ (anyth) (then can get all transactions involved from trans simple ms directly)
        corporate_name = info['listing_result']['corporate_name']
# from transaction get all transactions with listingID
        print('\n-----Retrieving transactions-----')
        listing_id = info['listing_result']['listing_id']
        transaction_URL_full = transaction_URL + f"/listing/{listing_id}"
        transaction_result = invoke_http(transaction_URL_full, method="GET", json=None)
        print('transaction_result:', transaction_result) #this returns a list of transactions
        subject = f"Your item collection has been cancelled!"
        if str(transaction_result) != "{'detail': 'Not Found'}":
            for transaction in transaction_result:
                #cannot test because the transaction does not make sense at the moment
                beneficiary_id = transaction['beneficiary_id']
                full_user_URL = user_URL + f"/beneficiary/{beneficiary_id}"
                beneficiary_result = invoke_http(full_user_URL, method='GET', json=None)
                username = beneficiary_result['username']
                email = beneficiary_result['email']
                message = f"Hi {username} aka {email}!<br><br>Your item - {info['listing_result']['name']} has been cancelled by {corporate_name}!<br>We apologize for any inconvinience caused<br><br>Thank you for using FreeBee!"
                sendEmail('lixuen.low.2021@scis.smu.edu.sg', subject, message);
        else:
            print("No transactions found")
# then go user and user details to send
#     #needs transaction objs, then hv a list of beneficiaryID
#     #needs to get userEmails + CompanyName
    # doEmail();

###################################################################
def doEmail():
    email = "lixuen.low.2021@scis.smu.edu.sg"
    subject = "test from FreeBee2222222222"
    message = "This is a test from FreeBee2222222!"
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(
    return sendEmail(email, subject, message);

def sendEmail(email, subject, message):
        print('<br>-----Invoking Email API-----')
        # full_sendEmail_URL = sendEmail_URL + "/" + email + "/" + subject + "/" + message
        print("calling callInvoke")
        full_sendEmail_URL = notification_URL + "/" + email
        toEmail = {'email': email, 'subject': subject, 'message': message}
        email_result = invoke_http(full_sendEmail_URL, method='GET', json=toEmail)
        print('email_result:', email_result)
        # loop.close()
        return email_result
###################################################################

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for the complex_notification...")
    app.run(host="0.0.0.0", port=5001, debug=True)
    # queues();
    # beginConsumption();
    