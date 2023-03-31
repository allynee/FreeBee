from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

listing_URL = "http://localhost:8000/listing"
geocoding_URL = "http://localhost:3000/"
notification_URL = "http://localhost:3000/"
authentication_URL = "http://localhost:3001/auth/checkaccess/"

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk3OWVkMTU1OTdhYjM1Zjc4MjljZTc0NDMwN2I3OTNiN2ViZWIyZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXNkZWV6bnV0eiIsImF1ZCI6ImVzZGVlem51dHoiLCJhdXRoX3RpbWUiOjE2Nzk5MzgxNTIsInVzZXJfaWQiOiI3TE5vaHMwWjBEVFYzWEo4VWJvNmtxR09GaXoxIiwic3ViIjoiN0xOb2hzMFowRFRWM1hKOFVibzZrcUdPRml6MSIsImlhdCI6MTY3OTkzODE1MiwiZXhwIjoxNjc5OTQxNzUyLCJlbWFpbCI6Ind0ZkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsid3RmQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.VoTsaM6gT-KeX7PRwtS3GdaMOjDp3SzXXhYeZjbw5l3h0x82IOiLjGN1cIZI9GYx_RfLtvrRi2dcpENI_H8QHAXdkMypfwm04H3f2fV5-q2ICpAYBCOdJt4C6kiMmq7wVXGKpNivCISSDl3cQRwfsNDJSPx4AUkLzMbKZZyEoxe26f0ubUbdkkj0GowW8qgLwlLgz4WsAeXOD7-WAIQgcuxZIVPUXLvdKV9bJee2Om9y19aHbjatiHNfrBKD4ZwouNc-6fGFVqwjd-WMbl7vTSFkNN9gQ4bCMff0vCuO5z6l-s-EB2ZT7WVCmYPPQMFfNxeIGSjs3GKC81WIxU_9UA"

@app.route("/listing_management", methods=['POST'])
def create_listing():
    #Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            listing = request.get_json()
            print("\nReceived an listing in JSON:", listing)        
         
            # do the actual work
            # 1. Create listing info 
            result = processCreateListing(listing, token)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "listing_management.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

@app.route("/listing_management/<int:listing_id>", methods=['PUT'])
def update_listing(listing_id):
    #Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            listing = request.get_json()
            print("\nReceived an listing in JSON:", listing)        
         
            # do the actual work
            # 1. Update listing info 
            result = processUpdateListing(listing, listing_id)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processCreateListing(listing, token):
    #2. authenticate that this is a corporate user

    authentication_result = authenticateUser(token) 
    print(authentication_result)

    if ("role" in authentication_result) and (authentication_result['role'] == "corporate"):
        # #3. send address string from listing to geocoding API
        # address = listing["address"]
        # geocoding_URL_full = geocoding_URL + address
        # #Invoke the geocoding microservice
        # print('\n-----Invoking geocoding microservice-----')
        # geocoding_result = invoke_http(geocoding_URL_full, method='GET', json=listing)

        # area = geocoding_result["area"]
        # district = geocoding_result["district"]
        # postal_code = geocoding_result["postal_code"]

        # listing["area"] = area
        # listing["district"] = district
        # listing["postal"] = postal_code

        print(listing) #check if area district and postal code was added to listing object

        #still need to implement logic check for whether geocoding was successful or not

        #4. Send the listing info to database
        #Invoke the listing microservice
        print('\n-----Invoking listing microservice-----')
        listing_result = invoke_http(listing_URL, method='POST', json=listing)
        print('listing_result:', listing_result)

        if "detail" not in listing_result: 

            #5. Send the notification to users who are subscribed to the corporate
            ############  Publish to subscribe queue   #############
            obj = {
                "listing_result": listing_result
            } 
            message = json.dumps(obj)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.subscribers", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print(f"sending message: {message} to queue 'subscribers' in Notification complex MS")

        else:
            print("failed creation of service")
            return {
                "code": 500,
                "message": "Creation of listing failed. Check if listing service is running."
            }, 500
    else:
        return {
            "code": 404,
            "message": "Unauthenticated user. User needs to be logged into a corporate account."
        }, 404

def processUpdateListing(listing, listing_id):
    #2.authenticate that this user is a corporate
    authentication_result = authenticateUser(token) 
    print(authentication_result)

    if ("role" in authentication_result) and (authentication_result['role'] == "corporate"):
        #3. Update listing info in the database
        #Invoke the listing microservice
        listing_URL_full = listing_URL + "/" + str(listing_id)
        print('\n-----Invoking listing microservice-----')
        listing_result = invoke_http(listing_URL_full, method='PUT', json=listing)
        print('listing_result:', listing_result)
    else:
        return {
            "code": 404,
            "message": "Unauthenticated user. User needs to be logged into a corporate account."
        }, 404

def authenticateUser(token_input):
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + token_input #need to get token from the front-end, currently HARDCODED
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)
    return authentication_result


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a listing...")
    app.run(host="0.0.0.0", port=5000, debug=True)