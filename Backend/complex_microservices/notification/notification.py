from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import asyncio
import time

# import amqp_setup
import pika
import json


app = Flask(__name__)
CORS(app)

# listing_URL = "http://localhost:8000/listing"
# geocoding_URL = "http://localhost:3000/"
# notification_URL = "http://localhost:3000/"
# authentication_URL = "localhost:3001/"
sendEmail_URL = "http://localhost:5005/sendmail"


@app.route("/", methods=['GET'])
###################################################################
def recieveMail():
    if request.is_json:
        try:
            info = request.get_json()
            print("\nReceived info in JSON:", info)        
         
            # do the actual work
            # 1. recieve info 
            result = sortMail()
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
    if info.purpose == "subscription":
        subscription(info)
    elif info.purpose == "toBeneficiary":
        toBeneficiary(info)
    elif info.purpose == "toCorporate":
        toCorporate(info)
    elif info.purpose == "cancel":
        cancel(info)

def subscription(info):
    doEmail();

def toBeneficiary(info):
    doEmail();

def toCorporate(info):
    doEmail();

def cancel(info):
    doEmail();

###################################################################
def doEmail():
    email = "lixuen.low.2021@scis.smu.edu.sg"
    subject = "test from FreeBee2222222222"
    message = "This is a test from FreeBee2222222!"
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(
    return sendEmail(email, subject, message);

def sendEmail(email, subject, message):
        print('\n-----Invoking listing microservice-----')
        # full_sendEmail_URL = sendEmail_URL + "/" + email + "/" + subject + "/" + message
        print("calling callInvoke")
        full_sendEmail_URL = sendEmail_URL + "/" + email
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
    