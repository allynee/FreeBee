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

transaction_URL = "http://localhost:9000/transaction"
listing_URL = "http://localhost:8000/listing"
authentication_URL = "http://localhost:3001/auth/checkaccess/"

status = "Cancelled"

@app.route("/transaction_management", methods=['POST'])
def create_transaction():
        # Simple check of input format and data of the request are JSON
        if request.is_json:
            try:
                required_details = request.get_json()
                print("\nJSON to create transaction:", required_details)
                # do the actual work
                # 1. initiate creation of transaction
                listing = required_details["listing"]
                beneficiary_id = required_details["beneficiary_id"]
                quantityDeducted = required_details["quantity"]
                token = required_details["token"]
                result = processCreateTransaction(listing, beneficiary_id, quantityDeducted, token)
                print('\n------------------------')
                print('\nresult: ', result)
                return jsonify(result)

            except Exception as e:
                # Unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 500,
                    "message": "transaction service internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400


@app.route("/transaction_management", methods=['PUT']) #assuming i get transaction and listing
def update_transaction():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            required_details = request.get_json()
            print("\nJSON with details to update in transaction:", required_details)
            listing = required_details["listing"]
            transaction = required_details["transaction"]
            token = required_details["token"]
            # do the actual work
            # 1. initiate update of transaction
            result = processUpdateTransaction(transaction, listing, token, status)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "transaction service internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

@app.route("/transaction_management/beneficiary/<string:beneficiary_id>", methods=["GET"])
def view_transactions_beneficiary(beneficiary_id):

    results = []

    #1. Retrieve transactions associated with beneficiary  
    print('\n-----Retrieving transactions-----')
    transaction_URL_full = transaction_URL + f"/beneficiary/{beneficiary_id}"
    transaction_result = invoke_http(transaction_URL_full, method="GET", json=None)
    print('transaction_result:', transaction_result)

    #2. For each transaction, retrieve listing details

    for transaction in transaction_result:
        listing_id = transaction["listing_id"]
        print('\n-----Retrieving listing details for each transaction-----')
        listing_URL_full = listing_URL + f"/{listing_id}"
        listing_result = invoke_http(listing_URL_full, method="GET", json=None)
        print('listing_result:', listing_result)
        
        #3. add listing details into each transaction
        transaction["listing_details"] = listing_result
        print('\nEdited transaction:', transaction)
        results.append(transaction)

    print(results)

    return {
        "code": 200,
        "message": "Retrieving transactions via beneficiary_id was successful",
        "result":  results
    }

@app.route("/transaction_management/corporate/<string:corporate_id>", methods=["GET"])
def view_transactions_corp(corporate_id):

    results = []

    #1. Retrieve transactions associated with corporate  
    print('\n-----Retrieving transactions-----')
    transaction_URL_full = transaction_URL + f"/corporate/{corporate_id}"
    transaction_result = invoke_http(transaction_URL_full, method="GET", json=None)
    print('transaction_result:', transaction_result)

    #2. For each transaction, retrieve listing details

    for transaction in transaction_result:
        listing_id = transaction["listing_id"]
        print('\n-----Retrieving listing details for each transaction-----')
        listing_URL_full = listing_URL + f"/{listing_id}"
        listing_result = invoke_http(listing_URL_full, method="GET", json=None)
        print('listing_result:', listing_result)
        
        #3. add listing details into each transaction
        transaction["listing_details"] = listing_result
        print('\nEdited transaction:', transaction)
        results.append(transaction)

    print(results)

    return {
        "code": 200,
        "message": "Retrieving transactions via corporate_id was successful",
        "result":  results
    }


def processCreateTransaction(listing, beneficiary_id, quantityDeducted, token):
    listing_id = listing["listing_id"]
    corporate_id = listing["corporate_id"]

    # 2. Authenticate user
    authentication_result = authenticateUser(token) 
    if authentication_result["statusCode"] == '200':
        if (authentication_result['role'] == "beneficiary"):
            
            # 3. Create the transaction info
            transaction = {
                "listing_id": listing_id,
                "corporate_id": corporate_id,
                "beneficiary_id": beneficiary_id,
                "status": "In Progress",
                "quantity": int(quantityDeducted)
            }
            #4. Check that beneficiary can deduct quantity requested from listing
            #4a. Get existing listing details
            # listing_URL_full = listing_URL + "/" + str(listing_id)
            # listing_result = invoke_http(listing_URL_full, method='GET', json=None)
            # print('listing_result:', listing_result)
            existing_quantity = int(listing["quantity"])
            #4b. Deduct quantity from  listing
            new_quantity = existing_quantity - int(quantityDeducted)
            new_listing = {"quantity": new_quantity}
            if new_quantity >= 0: #if sufficient quantity
                print('\n-----Updating listing-----')
                listing_URL_full = listing_URL + "/" + str(listing_id)
                listing_result = invoke_http(listing_URL_full, method='PUT', json=new_listing) 
                print('listing_result:', listing_result)
            else: #terminate process
                return{
                    "code": 500,
                    "message": "Insufficient quantity to claim."
                }, 500
            # 5. Invoke the transaction microservice
            print('\n-----Invoking transaction microservice-----')
            transaction_result = invoke_http(transaction_URL, method='POST', json=transaction)
            print('transaction_result:', transaction_result)
            return {
                "code": 200,
                "message": "Congrats transaction claim successful"
            }, 200
    else:
        return {
            "code": 404,
            "message": "Unauthenticated user. User needs to be logged into a beneficiary account."
        }, 404

def processUpdateTransaction(transaction, listing, token, status):

    listing_id = listing["listing_id"]

    #2. Authenticate user
    authentication_result = authenticateUser(token) 

    if authentication_result["statusCode"] == "200":

        transaction_id = transaction["transaction_id"]
        
        #3. Update transaction
        transaction_URL_full = transaction_URL + "/" + str(transaction_id)
        print('\n-----Invoking transaction microservice-----')
        transaction_update = {
            "status": status
        }
        transaction_result = invoke_http(transaction_URL_full, method='PUT', json=transaction_update)
        print('transaction_result:', transaction_result)    

        #4. Notify users if theres is a change in the status of the transaction

        #4a. If transaction is Cancelled from Corporate
        if transaction_result["status"] == "Cancelled":
            print('\n-----Send to Notification microservice-----')
            obj = {
                "purpose": "Cancelled",
                "listing_result": listing
            } 
            message = json.dumps(obj)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="cancel.notif", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print(f"sending message: {message} to 'cancel'")

        #4c. If items are Ready to Collect
        if transaction_result["status"] == "Ready to Collect":
            obj = {
                "purpose": "toBeneficiary",
                "listing_result": listing,
                "transaction_result": transaction
            }
            message = json.dumps(obj)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="ready.notif", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print(f"sending message: {message} to 'collect'")

        #5. Update Listing
        print('\n-----Updating listings-----')
        listing_URL_full = listing_URL + "/" + str(listing_id)
        listing_update = {
            "status": status
        }
        listing_result = invoke_http(listing_URL_full, method="PUT", json=listing_update)
        print('listing_result:', listing_result)

#create a function to display transactions associated with an id
# def processViewTransactions(user_id):
#     #2. Retrieve all transactions associated with user id, store status, ben id, corp id, listing id
#     #2a. Retrieve if corporate
#     #2b. Retrieve if beneficiary

#     transactions = ["transaction 1"]

#     #4. For each transaction
#     for transaction in transactions:
#         pass
#     #4a. Retrieve associated listing & listing details


def authenticateUser(token_input):
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + token_input #need to get token from the front-end, currently HARDCODED
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)
    return authentication_result

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a transaction...")
    app.run(host="0.0.0.0", port=5100, debug=True)