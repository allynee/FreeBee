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
listing_URL = "http://0.0.0.0:8000/listing"
listing_management_URL = "http://localhost:5000/listing_management"
authentication_URL = "http://localhost:3001/auth/checkaccess/"

transaction_status = "Ready to Collect"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk3OWVkMTU1OTdhYjM1Zjc4MjljZTc0NDMwN2I3OTNiN2ViZWIyZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXNkZWV6bnV0eiIsImF1ZCI6ImVzZGVlem51dHoiLCJhdXRoX3RpbWUiOjE2Nzk4NDgyNTUsInVzZXJfaWQiOiI3TE5vaHMwWjBEVFYzWEo4VWJvNmtxR09GaXoxIiwic3ViIjoiN0xOb2hzMFowRFRWM1hKOFVibzZrcUdPRml6MSIsImlhdCI6MTY3OTg0ODI1NSwiZXhwIjoxNjc5ODUxODU1LCJlbWFpbCI6Ind0ZkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsid3RmQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.GVt7An98raNHDDf3JFdQchehWMgfjSkAdJq8Gdr4mYPx6sJ2erboLBqb1iRLVUm0R_Uu3oOmqB2I3150MtQTo5LRlmQKdMb3XjZeOaWPztkviHEb7u3_SouQpR0WFN7UppziLM8omVQDMFVnb9jlSlHfp80u5tKWEeXmtnKIwhTVKTs7FvgoCPgycmKpJ7RYpH5soO46iwFO8s0onh7Hd74zDM1ZnjJpZjIuCx7_b27fmJWB8tp7RBnwTA0l5nsG450hlmpMTvTE6w3iuB_tJ39acGTCIfCQjGNCNUKwAfJeGhwEclTtMqyZ-ApBYQcO20TRMNZvjT5kj8k0V9zE1Q"


@app.route("/transaction_management", methods=['POST'])
def create_transaction():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            transaction = request.get_json()
            print("\nCreated a transaction in JSON:", transaction)

            # do the actual work
            # 1. initiate creation of transaction
            result = processCreateTransaction(transaction)
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
                "message": "create_transaction.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


@app.route("/transaction_management/<int:transaction_id>", methods=['PUT'])
def update_transaction(transaction_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            transaction = request.get_json()
            print("\nJSON with details to update in transaction:", transaction)

            # do the actual work
            # 1. initiate update of transaction
            result = processUpdateTransaction(transaction, transaction_id)
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

@app.route("/transaction_management/<int:user_id>", methods=['GET'])
def display_transactions(user_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # do the actual work
            # 1. initiate view of all transactions associated with user id
            result = processViewTransactions(user_id)
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

def processCreateTransaction(transaction, quantityDeducted):
    # 2. Authenticate user
    authentication_result = authenticateUser(token) 
    if authentication_result["statusCode"] == 200:
        if (authentication_result['role'] == "beneficiary"):
            # 3. Create the transaction info
            # Invoke the transaction microservice
            print('\n-----Invoking transaction microservice-----')
            transaction_result = invoke_http(transaction_URL, method='POST', json=transaction)
            print('transaction_result:', transaction_result)
            print('listing_id', transaction_result['listing_id'])

            listing_id = transaction_result['listing_id'] #get listing_id of newly created transaction

            #4. Update listing quantity
            print('\n-----Invoking listing  microservice-----') # access listing straight
            #4a. Get existing listing details
            listing_management_URL_full = listing_management_URL + "/" + str(listing_id)
            listing_result = invoke_http(listing_management_URL_full, method='GET', json=None)
            print('listing_result:', listing_result)
            existing_quantity = listing_result["quantity"]
            #4b. Deduct quantity from  listing
            new_quantity = existing_quantity - quantityDeducted
            new_listing = {"quantity": new_quantity}
            if new_quantity >= 0:
                listing_result = invoke_http(listing_management_URL, method='PUT', json=new_listing) 
            else:
                return{
                    "code": 500,
                    "message": "Insufficient quantity to claim."
                }, 500
    else:
        return {
            "code": 404,
            "message": "Unauthenticated user. User needs to be logged into a beneficiary account."
        }, 404

def processUpdateTransaction(transaction, transaction_id):

    #2. Authenticate user
    authentication_result = authenticateUser(token) 

    if authentication_result["statusCode"] == 200:

        #3. Update transaction
        transaction_URL_full = transaction_URL + "/" + str(transaction_id)
        print('\n-----Invoking transaction microservice-----')
        transaction_result = invoke_http(transaction_URL_full, method='PUT', json=transaction)
        print('transaction_result:', transaction_result)    

        #4. Notify users if theres is a change in the status of the transaction

        #4a. If transaction is Cancelled from Corporate
        if transaction_result["status"] == "Cancelled":
            obj = {} 
            message = json.dumps(obj)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.cancel", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print(f"sending message: {message} to queue 'cancel'")

        #4c. If items are Ready to Collect
        if transaction_result["status"] == "Ready to Collect":
            obj = {} 
            message = json.dumps(obj)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email.collect", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print(f"sending message: {message} to queue 'collect'")
                    

#create a function to display transactions associated with an id
def processViewTransactions(user_id):
    pass
    #2. Authenticate user, retrieve user type
    authentication_result = authenticateUser(token) 

    #3. Retrieve all transactions associated with user id, store status, ben id, corp id, listing id
    #3a. Retrieve if corporate
    #3b. Retrieve if beneficiary

    transactions = ["transaction 1"]

    #4. For each transaction
    for transaction in transactions:
        pass
    #4a. Retrieve associated beneficiary
    #4b. Retrieve associated corporate
    #4c. Retrieve associated listing & listing details

#create a function to delete transaction
def processDeleteTransaction(transaction_id):
    pass


def authenticateUser(token_input):
    print('\n-----Authenticating user-----')
    authentication_URL_full = authentication_URL + token_input #need to get token from the front-end, currently HARDCODED
    authentication_result = invoke_http(authentication_URL_full, method="GET", json=None)
    print('authentication_result:', authentication_result)
    return authentication_result

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for managing a transaction...")
    app.run(host="0.0.0.0", port=5100, debug=True)