from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

# import requests
from invokes import invoke_http

# import amqp_setup
# import pika
# import json

app = Flask(__name__)
CORS(app)

listing_URL = "http://localhost:8000/listing"
geocoding_URL = "http://localhost:8000/geocoding"

@app.route("/create_listing", methods=['POST'])
def create_listing():
    #Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            listing = request.get_json()
            print("\nReceived an listing in JSON:", listing)

            # do the actual work
            # 1. Create listing info 
            #result = processCreateListing(listing)
            result = testMSAccess(listing)
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

def testMSAccess(listing):
    print('\n-----Invoking listing microservice-----')
    listing_result = invoke_http(listing_URL, method='POST', json=listing)
    return {
        "data": {"listing_result": listing_result}
    }


def processCreateListing(listing):
    #2. send JSON to geocoding API
    #Invoke the geocoding microservice
    print('\n-----Invoking geocoding microservice-----')
    geocoding_result = invoke_http(geocoding_URL, method='GET', json=listing)

    #Check if geocoding result was successful; if successful then create listing
    code = geocoding_result["code"]
    message = json.dumps(geocoding_result)

    if code == 200:

        listing = geocoding_result["data"]
        #3. Send the listing info to database
        #Invoke the listing microservice
        print('\n-----Invoking listing microservice-----')
        listing_result = invoke_http(listing_URL, method='POST', json=listing)
        print('listing_result:', listing_result)

        #Check listing creation result; if successful then invoke notification service
        code = listing_result["code"]
        message = json.dumps(listing_result)

        if code == 200:
            #4. Create the notification
            # Invoke the notification service
            print('\n-----Invoking notification microservice-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="listing.notification", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            
            print("\nListing status ({:d}) published to the RabbitMQ Exchange:".format(
                code), listing_result)
            
            return {
                "code": 500,
                "data": {"listing_result": listing_result},
                "message": "Listing created, notification sent to subscribers."
            }
    
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a listing...")
    app.run(host="0.0.0.0", port=5000, debug=True)