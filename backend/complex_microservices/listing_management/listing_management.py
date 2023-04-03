from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

listing_URL = environ.get('listing_URL') or "http://localhost:8000/listing"
geocoding_URL = environ.get('geocoding_URL') or "http://localhost:3000/"
# notification_URL = environ.get('notification_URL') or "http://localhost:5005/"
authentication_URL = environ.get('auth_URL') or "http://localhost:3001/auth/checkaccess/"
image_URL = environ.get('image_URL') or "http://localhost:3002/image"


@app.route("/listing_management", methods=['POST'])
def create_listing():
    image_file = request.files['image']
    data = json.loads(request.form.get('data'))
    listing = json.loads(data['listing'])

    print('line32', listing)
    print(image_file)
    filename = image_file.filename
    tempdir = "/data"
    filepath = os.path.join(tempdir, filename)
    image_file.save(filepath)
    #Simple check of input format and data of the request are JSON
    if request.files:
        try:
            data = json.loads(request.form.get('data'))
            listing = json.loads(data['listing'])
            print("\nReceived an listing in JSON:", listing)  

            listing_object = listing

            token = data['token']
            # do the actual work
            # 1. Create listing info 
            json_filepath = json.dumps({"filepath": filepath,"filename":filename})
            result = processCreateListing(listing_object, token, json_filepath)
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

@app.route("/listing_management/<string:listing_id>", methods=['PUT'])
def update_listing(listing_id):
    #Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            request_json = request.get_json()
            listing = request_json['listing']
            print("\nReceived an listing in JSON:", listing) 
            token = request_json['token']
            # do the actual work
            # 1. Update listing info 
            result = processUpdateListing(listing, listing_id, token)
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

@app.route("/listing_managemen", methods=['GET']) #implement function to view all listings
def display_listings():
    list_of_listings = []
    #1. Retrieve all listings
    #Invoking the listing MS
    print('\n-----Retrieving listings-----')
    listing_result = invoke_http(listing_URL, method="GET", json=None)
    print('listing_result:', listing_result)

    for listing in listing_result:
        listing_id = listing["listing_id"]
        img_ext = listing["img_ext"]
        firebase_url = f"https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F{listing_id}{img_ext}?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4"
        listing_and_image = {
            "listing": listing,
            "firebase_url": firebase_url
        }
        list_of_listings.append(listing_and_image)
    return list_of_listings
    
def processCreateListing(listing_object, token, image):
    #2. authenticate that this is a corporate user
    authentication_result = authenticateUser(token) 

    if (authentication_result["statusCode"] == '200'):
        if (authentication_result['role'] == "corporate"):
            # #3. send address string from listing to geocoding API
            print('\n-----Invoking geocoding microservice-----')
            address = listing_object["address"]
            # geocoding_URL_full = "http://localhost:3000/graphql"
            geocoding_URL_full = geocoding_URL + "graphql"
            query = f'''query {{
                address(address: "{address}") {{
                    address
                    postal_code
                    area
                    district
                }}
            }}
            '''
            r = requests.post(geocoding_URL_full, json={'query': query})
            print(json.dumps(r.json()))
            r = r.json()

            area = r["data"]["address"]["area"]
            district = r["data"]["address"]["district"]
            postal_code =r["data"]["address"]["postal_code"]

            listing_object["area"] = area
            listing_object["district"] = int(district)
            listing_object["postal"] = int(postal_code)

            print(listing_object) #check if area district and postal code was added to listing object

            #4. Send the image data to database
            #Invoke the image microservice
            print('\n-----Invoking image microservice-----')
            image = eval(image)
            image_result = invoke_http(image_URL, method='POST', json=image)
            print('image_result:', image_result)
            #still need to check whether this is successful or not, ideally
            
            listing_object["listing_id"] = image_result['listingid']
            listing_object['img_ext']=  image_result['extension']
            print(listing_object)
            #5. Send the listing info to database
            #Invoke the listing microservice
            print('\n-----Invoking listing microservice-----')
            listing_result = invoke_http(listing_URL, method='POST', json=listing_object)
            print('listing_result:', listing_result)

        
            if "detail" not in listing_result: 
                #5. Send the notification to users who are subscribed to the corporate
                ############  Publish to subscribe queue   #############
                print('\n-----Sending notification to RabbitMQ-----')
                obj = {
                    "purpose": "subscription",
                    "listing_result": listing_result
                } 
                message = json.dumps(obj)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribers.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to queue 'subscribers' in Notification complex MS")

            else:
                return {
                    "code": 500,
                    "message": "Creation of listing failed. Check if listing service is running."
                }, 500
    else:
        return {
            "code": 404,
            "message": "Unauthenticated user. User needs to be logged into a corporate account."
        }, 404

def processUpdateListing(listing, listing_id,token):
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