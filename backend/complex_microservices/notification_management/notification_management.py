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
# notification_management_URL = "http://localhost:5001/" #this is this page
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
            return result #this is always None cus nvr return reply

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
        return subscription(info)
    elif info['purpose'] == "toBeneficiary":
        return toBeneficiary(info)
    elif info['purpose'] == "toCorporate":
        # print("toCorporate")
        return toCorporate(info)
    elif info['purpose'] == "cancelled":
        return cancel(info)

def subscription(info):
#     ############ This is for mass sending to all subscribers ## FROM listing_manage ##########
#     #Already has listing details + CompanyId
#     #needs to get userEmail + CompanyName
    print('<br>-----Invoking user microservice-----')
    corporate_id = info['listing_result']['corporate_id']
    print(corporate_id)
    full_user_URL = user_URL + f"/subscriber/corporate/{corporate_id}"
    subscription_result = invoke_http(full_user_URL, method='GET', json=None)
    print('subscription_result:', subscription_result) #this returns a list of the beneficiary info
    corporate_name =info['listing_result']['corporate_name']
    print("subscribers")
    if "detail" not in str(subscription_result):
        print('there are subs')
        result_codes = []
        for sub in subscription_result:
            ben_id = sub["beneficiary_id"]
            each_user_URL = user_URL + f"/beneficiary/" + ben_id
            sub_details = invoke_http(each_user_URL, method='GET', json=None)
            email = sub_details['email']
            username = sub_details['username']
            subject = f"{corporate_name} has posted a new listing!"
            message = f"Hi {username}! <br><br>{corporate_name} has posted a new listing! <br>Please check it out at http://localhost:8080/findFreeBee/{str(info['listing_result']['listing_id'])}<br><br>Thank you for using FreeBee!"
            print("calling sendEmail function")
            result = sendEmail(email, subject, message);
            result_codes += [result['code']]
        print(set(result_codes))
        if set(result_codes) == {200}:
            return {
                'code': 200,
                'message': "Successful sending to beneficiaries"
            }
        else:
            return {
                'code': 429,
                'message': "Not all beneficiaries were successfully sent an email"
            }
    else:
        return {
            'code': 400,
            'response': subscription_result,
            'message': "Unsuccessful call of transaction ms"
        }
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
    if 'detail' not in str(beneficiary_result):
        print('beneficiary_result:', beneficiary_result) #this returns a list of the beneficiary info
        email = beneficiary_result['email']
        username = beneficiary_result['username']
        if status == "In Progress":
            subject = f"Your claim is in progress!"
            message = f"Hi {username}!<br><br>You have successfully claimed an item - {info['listing_result']['name']}!<br>You may check the collection details in FreeBee and you'll be notified again when the item is ready for collection!<br><br>Thank you for using FreeBee!"
        if status == "Ready for Collection":
            subject = f"Your claim is ready for collection!"
            message = f"Hi {username}!<br><br>Your item - {info['listing_result']['name']} is ready for collection!<br>The collection details are as follows:<br>{info['listing_result']['collection_details']}<br>Collect at: {info['listing_result']['address']}, {info['listing_result']['postal']}<br><br>Thank you for using FreeBee!"
        if status == "Completed":
            subject = f"Your item has been successfully collected!"
            message = f"Hi {username}!<br><br>Your item - {info['listing_result']['name']} has been collected!<br><br>Thank you for using FreeBee!"
        # if status == "Cancelled":
        #     subject = f"Your item collection has been cancelled!"
        #     message = f"Hi {username}!<br><br>Your item - {info['listing_result']['name']} has been cancelled by {corporate_name}!<br>We apologize for any inconvinience caused<br><br>Thank you for using FreeBee!"
        result = sendEmail(email, subject, message);
        if result['code'] == 200:
            return {
                    'code': 200,
                    'message': "Successful sending to beneficiaries"
                }
        else:
            return {
                'code': 400,
                'response': result,
                'message': "sendEmail returned an error"
            }
    else:
        return {
                'code': 400,
                'response': beneficiary_result,
                'message': "Unsuccessful call of user ms"
            }



def toCorporate(info):
#     ############ This is for a specific company (successfulposting) ## FROM listing_manage ##########
#     #Already has listing details + CompanyId
#     #needs to get specificCompanyEmail + CompanyName
    print('<br>-----Invoking user microservice-----')
    corporate_id = info['listing_result']['corporate_id']
    print(corporate_id)
    full_user_URL = user_URL + f"/corporate/{corporate_id}"
    corporate_result = invoke_http(full_user_URL, method='GET', json=None)
    print('corporate_result:', corporate_result) #this returns coportate details
    if 'detail' not in str(corporate_result):
        corporate_name = info['listing_result']['corporate_name']
        email = corporate_result['email']
        print(info['listing_result']['quantity'])
        if info['listing_result']['quantity'] == 0:
            subject = f"Your listing has been fully claimed on Freebee!"
            message = f"Hi {corporate_name}! <br><br>Your listing - {info['listing_result']['name']} has been fully claimed on FreeBee!<br>Please check it out at http://localhost:8080/findFreeBee/{str(info['listing_result']['listing_id'])}<br><br>Thank you for using FreeBee!"
        else:
            subject = f"Successfully posted listing!"
            message = f"Hi {corporate_name}! <br><br>You have successfully posted a new listing - {info['listing_result']['name']}! <br><br>Thank you for using FreeBee!"
        result = sendEmail(email, subject, message);
        if result['code'] == 200:
            return {
                    'code': 200,
                    'message': "Successful sending to beneficiaries"
                }
        else:
            return {
                'code': 400,
                'response': result,
                'message': "sendEmail returned an error"
            }
    else:
        return {
                'code': 400,
                'response': corporate_result,
                'message': "Unsuccessful call of transaction ms"
            }

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
        if 'detail' not in str(transaction_result):
            result_codes = []
            for transaction in transaction_result:
                #cannot test because the transaction does not make sense at the moment
                beneficiary_id = transaction['beneficiary_id']
                full_user_URL = user_URL + f"/beneficiary/{beneficiary_id}"
                beneficiary_result = invoke_http(full_user_URL, method='GET', json=None)
                username = beneficiary_result['username']
                email = beneficiary_result['email']
                message = f"Hi {username}!<br><br>Your item - {info['listing_result']['name']} has been cancelled by {corporate_name}!<br>We apologize for any inconvinience caused.<br><br>Thank you for using FreeBee!"
                result = sendEmail(email, subject, message);
                result_codes += [result['code']]
            print(set(result_codes))
            if set(result_codes) == {200}:
                return {
                    'code': 200,
                    'message': "Successful sending to beneficiaries"
                }
            else:
                return {
                    'code': 429,
                    'message': "Not all beneficiaries were successfully sent an email"
                }
        else:
            return {
                'code': 400,
                'response': transaction_result,
                'message': "Unsuccessful call of transaction ms"
            }
# then go user and user details to send
#     #needs transaction objs, then hv a list of beneficiaryID
#     #needs to get userEmails + CompanyName
    # doEmail();

###################################################################
# def doEmail():
#     email = "lixuen.low.2021@scis.smu.edu.sg"
#     subject = "test from FreeBee2222222222"
#     message = "This is a test from FreeBee2222222!"
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(
#     return sendEmail(email, subject, message);

def sendEmail(email, subject, message):
        print('<br>-----Invoking Email API-----')
        # full_sendEmail_URL = sendEmail_URL + "/" + email + "/" + subject + "/" + message
        print("calling callInvoke")
        full_sendEmail_URL = notification_URL + "/" + email
        toEmail = {'email': email, 'subject': subject, 'message': message}
        email_result = invoke_http(full_sendEmail_URL, method='GET', json=toEmail)
        print('email_result:', email_result)
        if int(email_result["statusCode"]) not in range(200,300):
            return {
                'code': 400,
                'response': email_result,
                'message': "Unsuccessful call of notification ms"
            }
        else:
            return {
                'code': 200,
                'response': email_result,
                'message': "Successful call of notification ms"
            }

###################################################################

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for the complex_notification...")
    app.run(host="0.0.0.0", port=5001, debug=True)
    # queues();
    # beginConsumption();
    