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
authentication_URL = "localhost:3001/"

@app.route("/listing_management", methods=['POST'])
def create_listing():
    #Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            listing = request.get_json()
            print("\nReceived an listing in JSON:", listing)        
         
            # do the actual work
            # 1. Create listing info 
            result = processCreateListing(listing)
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

@app.route("/listing_management", methods=['GET'])
def get_listing():
    #1. get all listings
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL, method='GET', json=None)
    print('listing_result:', listing_result)
    return jsonify(listing_result)

@app.route("/listing_management/<int:listing_id>", methods=['GET'])
def get_specific_listing(listing_id):
    listing_URL_full = listing_URL + "/" + str(listing_id)
    #1. get specific listing
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL_full, method='GET', json=None)
    print('listing_result:', listing_result)
    return jsonify(listing_result)

@app.route("/listing_management/<int:listing_id>", methods=["DEL"])
def delete_listing(listing_id):
    listing_URL_full = listing_URL + "/" + str(listing_id)
    #1. delete specific listing
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL_full, method="DEL", json=None)
    print('listing deleted')
    return jsonify(listing_result)

def processCreateListing(listing):
    #2. authenticate that this is a corporate user
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + "auth/checkaccess/:token" #need to get token from the front-end
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)

    #3. send address string from listing to geocoding API
    address = listing["address"]
    geocoding_URL_full = geocoding_URL + address
    #Invoke the geocoding microservice
    print('\n-----Invoking geocoding microservice-----')
    geocoding_result = invoke_http(geocoding_URL_full, method='GET', json=listing)

    area = geocoding_result["area"]
    district = geocoding_result["district"]
    postal_code = geocoding_result["postal_code"]

    listing["area"] = area
    listing["district"] = district
    listing["postal"] = postal_code

    print(listing) #check if area district and postal code was added to listing object

    #4. Send the listing info to database
    #Invoke the listing microservice
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL, method='POST', json=listing)
    print('listing_result:', listing_result)

    #5. Send the notification to users who are subscribed to the corporate
    ############  Publish to subscribe queue   #############
    obj = {'CompanyName': "Salvation Army" ,
       'Subscribers': [{"email" : "lixuen.low.2021@scis.smu.edu.sg"}, {"email" : "llx16702@gmail.com"}]
       } 
    message = json.dumps(obj)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.subscribers", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))
    print(f"sending message: {message} to queue 'subscribers'")


def processUpdateListing(listing, listing_id):
    #2. Update listing info in the database
    #Invoke the listing microservice
    listing_URL_full = listing_URL + "/" + str(listing_id)
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL_full, method='PUT', json=listing)
    print('listing_result:', listing_result)

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a listing...")
    app.run(host="0.0.0.0", port=5000, debug=True)