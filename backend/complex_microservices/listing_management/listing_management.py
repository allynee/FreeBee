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

listing_URL = environ.get('listing_URL') or "http://localhost:8000/"
geocoding_URL = environ.get('geocoding_URL') or "http://localhost:3000/"
# notification_URL = environ.get('notification_URL') or "http://localhost:5005/"
authentication_URL = environ.get('auth_URL') or "http://localhost:3001/auth/checkaccess/"
image_URL = environ.get('image_URL') or "http://localhost:3002/image"
user_URL = environ.get('user_URL') or "http://localhost:8421/"

@app.route("/listing_management", methods=['POST'])
def create_listing():

    #Simple check of input format and data of the request are JSON
    if request.files:
        try:
            image_file = request.files['image']
            data = json.loads(request.form.get('data'))
            listing = json.loads(data['listing'])

            filename = image_file.filename
            tempdir = "/data"
            filepath = os.path.join(tempdir, filename)
            image_file.save(filepath)
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
            # listing['status'] = 'Unavailable'
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

@app.route("/listing_management", methods=['GET']) 
def display_listings():
    list_of_listings = []
    #1. Retrieve all listings
    #Invoking the listing MS
    print('\n-----Retrieving listings-----')
    listing_URL_FULL = listing_URL + "listing"
    listing_result = invoke_http(listing_URL_FULL, method="GET", json=None)
    if listing_result["code"] !=200:
        return {
            "code": listing_result["code"],
            "message": "listing service not invoked correctly"
        }
    print('listing_result:', listing_result)
    listing_result = listing_result["result"]

    print('\n-----Invoking Images-----')

    image_result = invoke_http(image_URL, method="GET", json=None)
    if image_result["code"] != 200:
        return{
            "code": image_result["code"],
            "message": "image service not invoked correctly"
        }
    print('image_result', image_result)
    image_result = image_result["result"]

    for listing in listing_result:
        listing_id = listing["listing_id"]
        img_ext = listing["img_ext"]
        firebase_url = image_result["front_url"] + listing_id + img_ext + image_result["back_url"]
        listing_and_image = {
            "listing": listing,
            "firebase_url": firebase_url
        }
        list_of_listings.append(listing_and_image)
    return list_of_listings
    

@app.route("/subscriptions/<string:beneficiary_id>", methods=['GET'])
def display_subscriptions(beneficiary_id):
    # list_of_subscriptions = []
    print("------ Retrieving Subscriptions ------")
    subscription_get_URL = user_URL + "subscription/beneficiary/" + beneficiary_id

    subscriptions = invoke_http(subscription_get_URL,method='GET',json=None)
    
    print("Subscription results: ",subscriptions)

    if subscriptions["code"] != 200:
        return {
            "code": subscriptions["code"],
            "message": "users microservice was not invoked properly"
        }

    subscriptions = subscriptions["result"]

    image_result = invoke_http(image_URL, method="GET", json=None)
    if image_result["code"] !=200:
        return {
            "code": image_result["code"],
            "message": "image service not invoked correctly."
        }
    image_result = image_result["result"]
    listings = []

    for subscription in subscriptions:
        corporate_id = subscription['corporate_id']
        listing_corporate_URL = listing_URL + "listings/" + corporate_id
        corporate_listings = invoke_http(listing_corporate_URL,method='GET',json=None)
        corporate_listings = corporate_listings["result"]
        for corporate_listing in corporate_listings:
            listing_id = corporate_listing["listing_id"]
            img_ext = corporate_listing["img_ext"]
            firebase_url = image_result["front_url"] + listing_id + img_ext + image_result["back_url"]
            return_listing = {'listing': corporate_listing,
                              "firebase_url": firebase_url}
            listings.append(return_listing)
    return listings

@app.route("/favourites/<string:beneficiary_id>", methods=['GET'])
def get_all_favourites(beneficiary_id):
    # list_of_subscriptions = []
    print("------ Retrieving Favourites ------")
    favourite_get_URL = user_URL + "all_favourite/" + beneficiary_id

    favourites = invoke_http(favourite_get_URL,method='GET',json=None)

    if favourites["code"]!=200:
        return {
            "code": favourites["code"],
            "message": "user service not invoked correctly" 
        }
    
    print("Favourites results: ",favourites)

    favourites = favourites["result"]

    listings = []

    for favourite in favourites:
        print(favourite)
        listing_id = favourite['listing_id']
        listing_id_URL = listing_URL + "listing/" + listing_id
        listing = invoke_http(listing_id_URL,method='GET',json=None)
        if listing["code"] != 200:
            return {
                "code": listing["code"],
                "message": "listing service not invoked correctly"
            }
        listing = listing["result"]
        img_ext = listing["img_ext"]
        image_result = invoke_http(image_URL, method="GET", json=None)
        if image_result["code"] != 200:
            return {
                "code": image_result["code"],
                "message": "image service not invoked correctly"
            }
        image_result = image_result["result"]

        firebase_url = image_result["front_url"] + listing_id + img_ext + image_result["back_url"]
        return_listing = {'listing': listing,
                        "firebase_url": firebase_url}
        listings.append(return_listing)
    return listings

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
                    code    
                    address
                    postal_code
                    area
                    district
                }}
            }}
            '''
            r = requests.post(geocoding_URL_full, json={'query': query})
            print('Geocoding Result:',json.dumps(r.json()))
            r = r.json()
            if(r['data']['address']['code']=="400"):
                return {
                    "code": 400,
                    "message": "Please enter the full address."
                }, 400
            

            area = r["data"]["address"]["area"]
            district = r["data"]["address"]["district"]
            postal_code =r["data"]["address"]["postal_code"]

            listing_object["area"] = area
            listing_object["district"] = int(district)
            listing_object["postal"] = int(postal_code)

            #4. Send the image data to database
            #Invoke the image microservice
            print('\n-----Invoking image microservice-----')
            image = eval(image)
            image_result = invoke_http(image_URL, method='POST', json=image)
            if image_result["code"] != 200:
                return {
                    "code": image_result["code"],
                    "result": image_result["result"]
                }
            image_result = image_result["result"]
            print('image_result:', image_result)   

            listing_object["listing_id"] = image_result['listingid']
            listing_object['img_ext']=  image_result['extension']
            
            print('Final JSON to post on listing: ',listing_object)

            #5. Send the listing info to database
            #Invoke the listing microservice
            print('\n-----Invoking listing microservice-----')
            listing_URL_FULL = listing_URL + "listing"
            listing_result = invoke_http(listing_URL_FULL, method="POST", json=listing_object)
            print('listing_result:', listing_result)

            if listing_result["code"] == 200: 
                #5. Send the notification to users who are subscribed to the corporate
                ############  Publish to subscribe queue   #############
                print('\n-----Sending notification to subscribers-----')
                obj = {
                    "purpose": "subscription",
                    "listing_result": listing_result["result"]
                } 
                message = json.dumps(obj)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribers.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to subscribers in Notification complex MS")

                print('\n-----Sending notification to corporate of successful listing-----')
                obj2 = {
                    "purpose": "toCorporate",
                    "listing_result": listing_result["result"]
                } 
                message = json.dumps(obj2)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="toCorporate.notif", 
                    body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print(f"sending message: {message} to corporate in Notification complex MS")
                return {"code": 200, "message": "Listing successful"},200

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

    if ("role" in authentication_result) and (authentication_result['role'] == "corporate"):
        #3. Update listing info in the database
        #Invoke the listing microservice
        listing_URL_full = listing_URL + "listing/" + str(listing_id)
        print('\n-----Invoking listing microservice-----')
        listing_result = invoke_http(listing_URL_full, method='PUT', json=listing)
        print('listing_result:', listing_result)
        if listing_result["code"] != 200:
            return {
                "code" : listing_result["code"],
                "result": listing_result["result"]
            }
        return {
            "code": 200,
            "result": listing_result["result"]
        }
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
    return authentication_result["result"]

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a listing...")
    app.run(host="0.0.0.0", port=5000, debug=True)