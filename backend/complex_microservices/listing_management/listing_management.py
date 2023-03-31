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

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk3OWVkMTU1OTdhYjM1Zjc4MjljZTc0NDMwN2I3OTNiN2ViZWIyZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXNkZWV6bnV0eiIsImF1ZCI6ImVzZGVlem51dHoiLCJhdXRoX3RpbWUiOjE2ODAyMzM5MzUsInVzZXJfaWQiOiIwdmJYemdGNW84U3pMWkxsS25WSGx0YTZyMVAyIiwic3ViIjoiMHZiWHpnRjVvOFN6TFpMbEtuVkhsdGE2cjFQMiIsImlhdCI6MTY4MDIzMzkzNSwiZXhwIjoxNjgwMjM3NTM1LCJlbWFpbCI6InRlc3QxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0MUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.etKySBOU7E53MmkhwrN9LcttQJ_2_1oSx9dzN0FmaEZrDDU_vz8i1OclcN_hfVjzoQHg1V9wMHAvEmwrriCi0r_hfPZzX4e4RuMLOSZb5ClHQyhCSujtKzKQncGOYlVH9nX9EjUkPqYdFoaN1jaTYhIXAbOb8tEGmWs44KvuL3_WQMiEb3aIcF_4TtmRiXLaijTR2o2bSvIVZJ360eyqrTXzUjHY2HPcW3t2gOthfyMswWPnhkROlLx8kzaprvOfN8kcoI1WAhRemrMHGVmNAoiUoaB6X69-pGy7fUgCD1lnIndUw1Nm9zblCHohy7oQZ9qb3KX0D-tIPPlRh0i1jg"

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

@app.route("/listing_management/", methods=['GET'])
def display_listings():
    pass
    #1. Retrieve all listings
    
        #2. Retrieve associated image

def processCreateListing(listing, token):
    #2. authenticate that this is a corporate user

    authentication_result = authenticateUser(token) 
    print(authentication_result)

    if (authentication_result["statusCode"] == 200):
        if (authentication_result['role'] == "corporate"):
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